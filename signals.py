"""
스윙 트레이딩 정량 스코어링 엔진
한국 5 + 미국 5 고정 종목에 대해 -100~+100 점수를 계산하고 매수/매도 신호를 판단한다.
"""
import os
import pandas as pd
import yfinance as yf

# ── 대상 종목 (한국 5 + 미국 5) ──────────────────────────────
TARGET_STOCKS = [
    {"ticker": "000660.KS", "name": "SK하이닉스",        "market": "한국", "sector": "반도체"},
    {"ticker": "005380.KS", "name": "현대차",            "market": "한국", "sector": "자동차"},
    {"ticker": "012450.KS", "name": "한화에어로스페이스", "market": "한국", "sector": "방산"},
    {"ticker": "035420.KS", "name": "NAVER",             "market": "한국", "sector": "플랫폼"},
    {"ticker": "068270.KS", "name": "셀트리온",          "market": "한국", "sector": "바이오"},
    {"ticker": "NVDA", "name": "Nvidia",    "market": "미국", "sector": "반도체"},
    {"ticker": "TSLA", "name": "Tesla",     "market": "미국", "sector": "자동차"},
    {"ticker": "META", "name": "Meta",      "market": "미국", "sector": "플랫폼"},
    {"ticker": "PLTR", "name": "Palantir",  "market": "미국", "sector": "AI소프트웨어"},
    {"ticker": "COIN", "name": "Coinbase",  "market": "미국", "sector": "금융/크립토"},
]

# ── 매매 규칙 상수 ────────────────────────────────────────────
BUY_THRESHOLD   = 40
SELL_THRESHOLD  = -40
STOP_LOSS_PCT   = -0.03   # 매수가 대비 -3% (고정% 폴백용, 아래 ATR 기준이 우선)
TAKE_PROFIT_PCT = 0.06    # 1차 익절 +6% (고정% 폴백용)
TRAILING_PCT    = -0.04   # 고점 대비 -4% 트레일링스탑 (고정% 폴백용)
# in-sample/out-of-sample을 나눠 그리드서치한 결과, 보유기한을 늘릴수록 in-sample 성과만
# 계속 좋아지고 out-sample은 나빠지는 과최적화 패턴 확인 (20일: 샤프 in2.07/out0.41).
# in/out 괴리가 가장 작으면서 out-sample 손익비·기대값이 가장 좋은 지점은 7일.
MAX_HOLD_DAYS   = 7       # 목표 미도달 시 강제 재평가

# 종목별 변동성(ATR)에 비례한 손절/익절 — 백테스트 결과 고정%은 변동성 큰 종목에서
# 진입 당일 정상 등락폭에 손절되는 비중이 84%에 달해 ATR 기준으로 대체
ATR_PERIOD          = 14
STOP_ATR_MULT        = 1.5   # 손절 = 진입가 - 1.5×ATR
TARGET_ATR_MULT      = 3.0   # 1차 익절 = 진입가 + 3.0×ATR (손익비 1:2 유지)
TRAILING_ATR_MULT    = 2.0   # 트레일링 = 고점 - 2.0×ATR

BASE_WEIGHTS = {
    "trend":  0.25,
    "macd":   0.20,
    "rsi":    0.20,
    "bb":     0.15,
    "volume": 0.10,
    "news":   0.10,
}


def _clip(x, lo=-1.0, hi=1.0):
    return max(lo, min(hi, x))


def calc_rsi(close, period=14):
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(period).mean()
    loss = -delta.where(delta < 0, 0).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def calc_macd(close, fast=12, slow=26, signal=9):
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    return macd_line, signal_line, macd_line - signal_line


def calc_atr(hist, period=ATR_PERIOD):
    high, low, close = hist["High"], hist["Low"], hist["Close"]
    prev_close = close.shift(1)
    true_range = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs(),
    ], axis=1).max(axis=1)
    return true_range.rolling(period).mean()


def calc_bollinger(close, period=20, num_std=2):
    mid = close.rolling(period).mean()
    std = close.rolling(period).std()
    upper = mid + num_std * std
    lower = mid - num_std * std
    percent_b = (close - lower) / (upper - lower)
    return upper, mid, lower, percent_b


# ── 하위 점수 계산 (-1 ~ +1) ──────────────────────────────────
def score_trend(price, ma20, ma60):
    price_gap = (price - ma20) / ma20
    ma_gap = (ma20 - ma60) / ma60
    raw = 0.5 * price_gap + 0.5 * ma_gap
    return _clip(raw / 0.05)  # 5% 괴리에서 만점


def score_macd(hist_value, price):
    return _clip(hist_value / (price * 0.01))  # 가격의 1%에서 만점


def score_rsi(rsi):
    return _clip((50 - rsi) / 50)  # RSI 0→+1(과매도=매수 우호), 100→-1(과매수=매도 우호)


def score_bb(percent_b):
    return _clip((0.5 - percent_b) * 2)


def score_volume(vol_ratio, price_change_pct):
    direction = 1 if price_change_pct >= 0 else -1
    return _clip(vol_ratio - 1.0) * direction


def score_news(ticker, news_items):
    """Claude로 뉴스 헤드라인 감성을 -1~+1로 평가. API 키/뉴스 없으면 중립(0)."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key or not news_items:
        return 0.0
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        headlines = "\n".join(news_items[:8])
        prompt = (
            f"다음은 {ticker}에 대한 최근 뉴스 헤드라인이다. "
            "이 뉴스들의 전반적 투자 심리를 -1.0(매우 부정적)부터 +1.0(매우 긍정적) 사이 "
            "숫자 하나로만 답하라. 다른 텍스트는 출력하지 마라.\n\n" + headlines
        )
        msg = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=10,
            messages=[{"role": "user", "content": prompt}],
        )
        return _clip(float(msg.content[0].text.strip()))
    except Exception:
        return 0.0


def adjust_weights(weights, trend_score):
    """강한 추세장에서는 역추세 지표(RSI) 비중을 줄이고 추세/모멘텀 비중을 늘린다."""
    weights = dict(weights)
    if abs(trend_score) > 0.6 and "rsi" in weights:
        shift = min(0.10, weights["rsi"])
        weights["rsi"] -= shift
        weights["trend"] = weights.get("trend", 0) + shift / 2
        weights["macd"] = weights.get("macd", 0) + shift / 2
    return weights


# 뉴스 데이터가 없는 경우(백테스트 등) 사용할, news 비중을 나머지에 재분배한 가중치
NO_NEWS_WEIGHTS = {
    k: v / (1 - BASE_WEIGHTS["news"]) for k, v in BASE_WEIGHTS.items() if k != "news"
}


def compute_technical_subscores(hist):
    """hist: 최소 60일치 OHLCV DataFrame (마지막 행 = 평가 시점). 뉴스 제외 하위점수를 반환."""
    close = hist["Close"]
    price = float(close.iloc[-1])
    ma20 = float(close.rolling(20).mean().iloc[-1])
    ma60 = float(close.rolling(60).mean().iloc[-1])
    rsi = float(calc_rsi(close).iloc[-1])
    _, _, macd_hist = calc_macd(close)
    macd_val = float(macd_hist.iloc[-1])
    _, _, _, percent_b = calc_bollinger(close)
    pb = float(percent_b.iloc[-1])

    today_vol = float(hist["Volume"].iloc[-1])
    avg_vol_20 = float(hist["Volume"].iloc[-21:-1].mean())
    vol_ratio = today_vol / avg_vol_20 if avg_vol_20 > 0 else 1.0
    price_change_pct = float(close.pct_change().iloc[-1] * 100)

    sub = {
        "trend": score_trend(price, ma20, ma60),
        "macd": score_macd(macd_val, price),
        "rsi": score_rsi(rsi),
        "bb": score_bb(pb),
        "volume": score_volume(vol_ratio, price_change_pct),
    }
    return sub, price, rsi, ma20, ma60


def compute_score(ticker, period="6mo"):
    hist = yf.Ticker(ticker).history(period=period)
    if len(hist) < 60:
        raise ValueError(f"{ticker}: 데이터 부족 ({len(hist)}일)")

    sub, price, rsi, ma20, ma60 = compute_technical_subscores(hist)
    atr = float(calc_atr(hist).iloc[-1])

    news_items = []
    try:
        for n in (yf.Ticker(ticker).news or [])[:8]:
            title = n.get("content", {}).get("title")
            if title:
                news_items.append(title)
    except Exception:
        pass
    sub["news"] = score_news(ticker, news_items)

    weights = adjust_weights(BASE_WEIGHTS, sub["trend"])
    total = sum(sub[k] * weights[k] for k in weights) * 100

    if total >= BUY_THRESHOLD:
        signal = "매수"
    elif total <= SELL_THRESHOLD:
        signal = "매도"
    else:
        signal = "관망"

    return {
        "ticker": ticker,
        "price": price,
        "score": round(total, 1),
        "signal": signal,
        "sub_scores": {k: round(v, 2) for k, v in sub.items()},
        "weights": weights,
        "stop_loss": round(price - STOP_ATR_MULT * atr, 2),
        "take_profit": round(price + TARGET_ATR_MULT * atr, 2),
        "atr": round(atr, 2),
        "data_date": hist.index[-1].strftime("%Y-%m-%d"),
        "rsi": round(rsi, 1),
        "ma20": round(ma20, 2),
        "ma60": round(ma60, 2),
    }


def scan_all():
    results = []
    for s in TARGET_STOCKS:
        try:
            r = compute_score(s["ticker"])
            r.update({"name": s["name"], "market": s["market"], "sector": s["sector"]})
            results.append(r)
        except Exception as e:
            print(f"⚠️ {s['name']}({s['ticker']}) 계산 실패: {e}")
    return sorted(results, key=lambda r: r["score"], reverse=True)


if __name__ == "__main__":
    rows = scan_all()
    print(f"{'종목':10} {'티커':10} {'현재가':>12} {'점수':>7} {'신호':>4}  섹터")
    for r in rows:
        print(f"{r['name']:10} {r['ticker']:10} {r['price']:>12,.0f} {r['score']:>7.1f} {r['signal']:>4}  {r['sector']}")
