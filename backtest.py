"""
signals.py의 스코어링 규칙을 과거 일봉 데이터에 되돌려 검증하는 백테스트 엔진.
뉴스 감성은 과거 헤드라인을 구할 수 없어 제외하고, 나머지 5개 지표 비중을 재분배해 평가한다.
매일 종가 기준으로 스코어를 계산하고, 신호 발생 다음날 시가에 체결하는 방식으로
룩어헤드 바이어스(미래 데이터 참조)를 피한다.
"""
from functools import lru_cache

import pandas as pd
import yfinance as yf
from datetime import datetime

from signals import (
    TARGET_STOCKS, NO_NEWS_WEIGHTS, BUY_THRESHOLD, MAX_HOLD_DAYS,
    STOP_ATR_MULT, TARGET_ATR_MULT, TRAILING_ATR_MULT,
    compute_technical_subscores, adjust_weights, calc_atr,
)

WARMUP_DAYS = 65     # MA60 등 지표 안정화에 필요한 최소 과거일수
OOS_MONTHS = 6       # out-of-sample(최근) 구간 — 과최적화 확인용
RISK_PER_TRADE = 0.15  # 거래당 자본 투입 비중 가정 (누적수익률 산출용, 동시보유 미반영 단순화)

# 왕복(매수+매도) 거래비용 가정 — 증권사/체결환경마다 다르므로 실사용 조건에 맞춰 조정할 것
COST_KR = 0.0003 + 0.0015 + 0.0010   # 수수료 왕복 0.03% + 증권거래세(매도) 0.15% + 슬리피지 왕복 0.10%
COST_US = 0.0014 + 0.0010            # 수수료 왕복 0.14% + 슬리피지 왕복 0.10%


def cost_for(ticker):
    return COST_KR if ticker.endswith((".KS", ".KQ")) else COST_US


@lru_cache(maxsize=None)
def _fetch_history(ticker, period):
    return yf.Ticker(ticker).history(period=period)


def _score_at(hist, end_idx, base_weights=NO_NEWS_WEIGHTS):
    window = hist.iloc[max(0, end_idx - 250):end_idx + 1]  # 계산량 절감용 슬라이딩 윈도우
    try:
        sub, price, *_ = compute_technical_subscores(window)
        weights = adjust_weights(base_weights, sub["trend"])
        score = sum(sub[k] * weights[k] for k in weights) * 100
        if pd.isna(score):
            return 0.0, price
        return score, price
    except Exception:
        return 0.0, float(hist.iloc[end_idx]["Close"])


def simulate_ticker(ticker, period="3y", max_hold_days=MAX_HOLD_DAYS,
                     weights=NO_NEWS_WEIGHTS, buy_threshold=BUY_THRESHOLD):
    hist = _fetch_history(ticker, period)
    if len(hist) < WARMUP_DAYS + 30:
        return []
    atr_series = calc_atr(hist)

    trades = []
    n = len(hist)
    in_position = False
    entry_idx = entry_price = stop_price = target_price = atr_at_entry = None
    trailing_active = False
    trailing_high = None

    for i in range(WARMUP_DAYS, n - 1):
        row = hist.iloc[i]

        if in_position:
            exit_price = exit_reason = None

            if not trailing_active:
                if row["Low"] <= stop_price:
                    exit_price, exit_reason = stop_price, "손절"
                elif row["High"] >= target_price:
                    trailing_active = True
                    trailing_high = row["High"]
            else:
                trailing_high = max(trailing_high, row["High"])
                trail_stop = trailing_high - TRAILING_ATR_MULT * atr_at_entry
                if row["Low"] <= trail_stop:
                    exit_price, exit_reason = trail_stop, "트레일링청산"

            hold_days = i - entry_idx
            if exit_price is None and not trailing_active and hold_days >= max_hold_days:
                score, _ = _score_at(hist, i, weights)
                if score < buy_threshold:
                    exit_price, exit_reason = float(row["Close"]), "보유기한만료"

            if exit_price is not None:
                ret_gross = (exit_price - entry_price) / entry_price
                ret_net = ret_gross - cost_for(ticker)
                trades.append({
                    "ticker": ticker,
                    "entry_date": hist.index[entry_idx].strftime("%Y-%m-%d"),
                    "exit_date": hist.index[i].strftime("%Y-%m-%d"),
                    "entry_price": entry_price, "exit_price": exit_price,
                    "return_pct": ret_net * 100, "gross_return_pct": ret_gross * 100,
                    "reason": exit_reason, "hold_days": hold_days,
                })
                in_position = False
            continue  # 포지션 보유 중엔 신규 진입 판단 생략

        score, _ = _score_at(hist, i, weights)
        if score >= buy_threshold:
            atr_now = atr_series.iloc[i]
            if pd.isna(atr_now) or atr_now <= 0:
                continue  # ATR 계산 불가 구간은 진입 보류
            entry_idx = i + 1
            entry_price = float(hist.iloc[i + 1]["Open"])
            atr_at_entry = float(atr_now)
            stop_price = entry_price - STOP_ATR_MULT * atr_at_entry
            target_price = entry_price + TARGET_ATR_MULT * atr_at_entry
            trailing_active = False
            trailing_high = None
            in_position = True

    if in_position:  # 백테스트 종료 시점까지 열려있던 포지션 강제 청산
        last = hist.iloc[-1]
        ret_gross = (float(last["Close"]) - entry_price) / entry_price
        ret_net = ret_gross - cost_for(ticker)
        trades.append({
            "ticker": ticker,
            "entry_date": hist.index[entry_idx].strftime("%Y-%m-%d"),
            "exit_date": hist.index[-1].strftime("%Y-%m-%d"),
            "entry_price": entry_price, "exit_price": float(last["Close"]),
            "return_pct": ret_net * 100, "gross_return_pct": ret_gross * 100,
            "reason": "백테스트종료", "hold_days": (n - 1) - entry_idx,
        })

    return trades


def run_backtest(period="3y", oos_months=OOS_MONTHS, max_hold_days=MAX_HOLD_DAYS,
                  weights=NO_NEWS_WEIGHTS, buy_threshold=BUY_THRESHOLD):
    all_trades = []
    for s in TARGET_STOCKS:
        try:
            trades = simulate_ticker(s["ticker"], period=period, max_hold_days=max_hold_days,
                                      weights=weights, buy_threshold=buy_threshold)
            for t in trades:
                t["name"] = s["name"]
            all_trades.extend(trades)
        except Exception as e:
            print(f"⚠️ {s['name']}({s['ticker']}) 백테스트 실패: {e}")

    all_trades.sort(key=lambda t: t["exit_date"])
    cutoff = (datetime.now() - pd.DateOffset(months=oos_months)).strftime("%Y-%m-%d")
    in_sample = [t for t in all_trades if t["exit_date"] < cutoff]
    out_sample = [t for t in all_trades if t["exit_date"] >= cutoff]
    return all_trades, in_sample, out_sample


def compute_metrics(trades):
    if not trades:
        return None

    rets = [t["return_pct"] for t in trades]
    wins = [r for r in rets if r > 0]
    losses = [r for r in rets if r <= 0]
    win_rate = len(wins) / len(rets) * 100
    avg_win = sum(wins) / len(wins) if wins else 0
    avg_loss = sum(losses) / len(losses) if losses else 0
    profit_factor = (sum(wins) / abs(sum(losses))) if losses and sum(losses) != 0 else float("inf")
    expectancy = sum(rets) / len(rets)

    equity = [1.0]
    for r in rets:
        equity.append(equity[-1] * (1 + (r / 100) * RISK_PER_TRADE))
    peak = equity[0]
    max_dd = 0.0
    for e in equity:
        peak = max(peak, e)
        max_dd = min(max_dd, (e - peak) / peak)
    total_return = (equity[-1] - 1) * 100

    span_days = (pd.to_datetime(trades[-1]["exit_date"]) - pd.to_datetime(trades[0]["entry_date"])).days
    years = max(span_days / 365, 0.25)
    trades_per_year = len(rets) / years
    std = pd.Series(rets).std()
    sharpe_approx = (expectancy / std * (trades_per_year ** 0.5)) if std else 0

    reasons = pd.Series([t["reason"] for t in trades]).value_counts().to_dict()

    return {
        "trades": len(rets), "win_rate": win_rate, "avg_win": avg_win, "avg_loss": avg_loss,
        "profit_factor": profit_factor, "expectancy": expectancy, "total_return": total_return,
        "max_dd": max_dd * 100, "sharpe": sharpe_approx, "reasons": reasons,
    }


def summarize(trades, label):
    m = compute_metrics(trades)
    if m is None:
        print(f"\n[{label}] 거래 없음")
        return

    print(f"\n[{label}] 거래 {m['trades']}건")
    print(f"  승률: {m['win_rate']:.1f}%   평균수익: {m['avg_win']:+.2f}%   평균손실: {m['avg_loss']:+.2f}%")
    print(f"  손익비(Profit Factor): {m['profit_factor']:.2f}   기대값(건당 평균): {m['expectancy']:+.2f}%")
    print(f"  누적수익률(거래당 자본 {RISK_PER_TRADE*100:.0f}% 투입 가정): {m['total_return']:+.1f}%   최대낙폭(MDD): {m['max_dd']:.1f}%")
    print(f"  근사 샤프비율(거래빈도 기반 연환산): {m['sharpe']:.2f}")
    print(f"  청산사유 분포: {m['reasons']}")


if __name__ == "__main__":
    all_trades, in_sample, out_sample = run_backtest()
    print(f"총 거래 {len(all_trades)}건 (최근 3년, 10종목 합산)")
    summarize(in_sample, "In-sample (과거~최근 6개월 전)")
    summarize(out_sample, f"Out-of-sample (최근 {OOS_MONTHS}개월, 과최적화 검증용)")
    summarize(all_trades, "전체 합산")
