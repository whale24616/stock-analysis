"""
매일 아침 자동 실행 — 4개 종목 AI 분석 후 이메일 + 카카오 발송
"""
import os, json, smtplib, requests, re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone, timedelta
import yfinance as yf
import anthropic

# ── 설정 ──────────────────────────────────────────────────────
GMAIL_USER   = "leero1126@gmail.com"
GMAIL_APP_PW = "xmpqsmeoexymwabm"
SEND_TO      = "leero1126@gmail.com"

ANTHROPIC_API_KEY    = os.environ.get("ANTHROPIC_API_KEY", "").strip()
KAKAO_ACCESS_TOKEN   = os.environ.get("KAKAO_ACCESS_TOKEN", "").strip()
KAKAO_REFRESH_TOKEN  = os.environ.get("KAKAO_REFRESH_TOKEN", "").strip()
KAKAO_REST_API_KEY   = os.environ.get("KAKAO_REST_API_KEY", "").strip()
KAKAO_CLIENT_SECRET  = os.environ.get("KAKAO_CLIENT_SECRET", "").strip()

KST = timezone(timedelta(hours=9))

# ── 분석할 4개 종목 ────────────────────────────────────────────
STOCKS = [
    {"ticker": "005930.KS", "name": "삼성전자",  "market": "한국"},
    {"ticker": "000660.KS", "name": "SK하이닉스", "market": "한국"},
    {"ticker": "NVDA",      "name": "NVIDIA",    "market": "미국"},
    {"ticker": "AAPL",      "name": "Apple",     "market": "미국"},
]

# ── 카카오 토큰 갱신 ───────────────────────────────────────────
def refresh_kakao_token():
    try:
        res = requests.post("https://kauth.kakao.com/oauth/token", data={
            "grant_type":    "refresh_token",
            "client_id":     KAKAO_REST_API_KEY,
            "client_secret": KAKAO_CLIENT_SECRET,
            "refresh_token": KAKAO_REFRESH_TOKEN,
        })
        data = res.json()
        print(f"🔑 카카오 토큰 갱신 응답: {data}")
        new_token = data.get("access_token", "")
        if new_token:
            return new_token.strip()
        else:
            print(f"⚠️ 토큰 갱신 실패, 기존 토큰 사용")
            return KAKAO_ACCESS_TOKEN
    except Exception as e:
        print(f"⚠️ 토큰 갱신 예외: {e}")
        return KAKAO_ACCESS_TOKEN

# ── 카카오 특수문자 제거 ───────────────────────────────────────
def clean_for_kakao(text):
    text = re.sub(r'\*+', '', text)
    text = re.sub(r'#+\s*', '', text)
    text = re.sub(r'~~.*?~~', '', text)
    text = re.sub(r'`+', '', text)
    text = re.sub(r'\[END\]', '', text)
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

# ── 카카오 나에게 보내기 ────────────────────────────────────────
def send_kakao(text, access_token):
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    access_token = access_token.strip().replace('\n','').replace('\r','').replace(' ','')
    clean_text = clean_for_kakao(text)

    # 카카오 텍스트 메시지 최대 9000자 (넉넉하게 활용)
    if len(clean_text) > 8500:
        clean_text = clean_text[:8500] + "\n\n[이하 이메일 참조]"

    template_str = json.dumps({
        "object_type": "text",
        "text": clean_text,
        "link": {
            "web_url": "https://stock-analysis-yhsctlbfdbbhzjbtbm8y6z.streamlit.app",
            "mobile_web_url": "https://stock-analysis-yhsctlbfdbbhzjbtbm8y6z.streamlit.app"
        }
    }, ensure_ascii=True)

    print(f"🔑 사용 토큰 앞 10자리: {access_token[:10]}...")
    res = requests.post(
        url,
        headers={"Authorization": f"Bearer {access_token}"},
        data={"template_object": template_str}
    )
    return res.json()

# ── 이메일 발송 ────────────────────────────────────────────────
def send_email(subject, html_body):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = GMAIL_USER
    msg["To"]      = SEND_TO
    msg.attach(MIMEText(html_body, "html", "utf-8"))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_APP_PW)
        server.send_message(msg)

# ── RSI 계산 ───────────────────────────────────────────────────
def calc_rsi(series, period=14):
    delta = series.diff()
    gain  = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss  = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs    = gain / loss
    return (100 - (100 / (1 + rs))).iloc[-1]

# ── 데이터 신뢰도 검증 ─────────────────────────────────────────
def validate_data(hist, name):
    if hist.empty:
        return False, "데이터 없음"
    last_date = hist.index[-1]
    # timezone-aware 처리
    if hasattr(last_date, 'tzinfo') and last_date.tzinfo is not None:
        now = datetime.now(last_date.tzinfo)
    else:
        now = datetime.now()
        last_date = last_date.replace(tzinfo=None)
    days_old = (now - last_date).days
    if days_old > 5:
        return False, f"데이터가 {days_old}일 전 데이터 (너무 오래됨)"
    return True, f"최신 데이터 확인 ({last_date.strftime('%Y-%m-%d')})"

# ── AI 분석 ────────────────────────────────────────────────────
def get_analysis(ticker, name, market, price, ma20, ma60, rsi, data_date, news_text="※ 뉴스 없음"):
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    now_kst   = datetime.now(KST)
    now_str   = now_kst.strftime('%Y년 %m월 %d일 %H시 %M분 (KST)')
    ma20_gap  = ((price - ma20) / ma20 * 100) if ma20 else 0
    ma60_gap  = ((price - ma60) / ma60 * 100) if ma60 else 0
    rsi_label = "과매수" if rsi >= 70 else ("과매도" if rsi <= 30 else "중립")
    kr_market = market == "한국"
    section1  = "1. 🌏 전일 미국 시장 분석 및 국내외 거시경제 환경" if kr_market else "1. 🌏 글로벌 시장 환경 및 거시경제 영향 요소"

    prompt = f"""당신은 10년 경력의 주식 애널리스트입니다. 한국어로 핵심 투자 판단 리포트를 작성하세요.

⚠️ 절대 규칙:
- 아래 【실시간 데이터】와 【최근 뉴스】에 있는 내용만 근거로 사용
- 뉴스에 없는 사실을 추측하거나 만들어내지 말 것
- 확인 안 된 정보는 "미확인" 또는 "뉴스 없음"으로 표기
- 4개 항목 완성 후 [END] 표시

【발송 시각】: {now_str} | 【데이터 기준일】: {data_date}
【종목】: {name} ({ticker})
【현재가】: {price:,.0f} | MA20: {ma20:,.0f} ({ma20_gap:+.1f}%) | MA60: {ma60:,.0f} ({ma60_gap:+.1f}%) | RSI: {rsi:.1f} ({rsi_label})

【최근 뉴스 (Yahoo Finance 실시간) — 이 내용만 사용】:
{news_text}

1. 📰 최근 뉴스 & 여론
위 뉴스 기반 최근 2건 요약 (날짜·사실 위주, 2문장). 뉴스 없으면 "현재 확인된 뉴스 없음"으로만 표기.

2. 📊 주가 흐름 분석
위 수치(현재가/MA20/MA60/RSI)만 활용해 3~4문장 분석. 수치 반드시 포함.

3. 🔗 연관 종목
같은 섹터 대표 종목 3개. 동향은 위 뉴스 기반으로만, 없으면 "동향 미확인".

4. ✅ 최종 투자 의견

결론: "[매수/매도/관망]" — 한 줄 요약

근거:
- 근거 1 (수치 기반)
- 근거 2 (뉴스 기반, 없으면 기술적 지표)
- 근거 3

투자 가이드라인:
| 항목 | 수치 |
|------|------|
| 목표가 (3개월) | 구체적 가격 (+상승률%) |
| 손절가 | 구체적 가격 (-하락률%) |
| 추천 진입가 | 구체적 가격 |
| 포지션 사이징 | 전체 자금의 X~Y% |
| 보유 기간 | X~Y개월 |

실행 방안:
1. 즉시 행동: 기존 보유자 조언
2. 대기 투자자: 진입 조건
3. 적극 공격자: 추가 진입 조건
4. 손실 관리: 손절 기준
"""
    msg = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}]
    )
    text = msg.content[0].text
    # [END] 없으면 결론이 잘린 것 — 마무리 문구 추가
    if "[END]" not in text:
        text += "\n\n✅ [분석 완료]"
    else:
        text = text.replace("[END]", "").strip()
    return text

# ── HTML 리포트 생성 ───────────────────────────────────────────
def make_html_report(stock_reports, run_time):
    cards = ""
    for r in stock_reports:
        analysis_html = r["analysis"].replace("\n", "<br>")
        # 마크다운 볼드 → HTML
        analysis_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', analysis_html)
        cards += f"""
        <div style='background:#fff; border:1px solid #e0e8f5; border-radius:16px;
                    padding:30px; margin-bottom:28px;
                    box-shadow:0 4px 20px rgba(21,101,192,0.07);'>
            <div style='display:flex; align-items:center; margin-bottom:12px;'>
                <span style='font-size:20px; font-weight:800; color:#0d47a1;'>
                    📈 {r['name']}
                </span>
                <span style='margin-left:10px; font-size:13px; color:#90a4ae;
                             background:#f0f4ff; padding:3px 10px; border-radius:20px;'>
                    {r['ticker']}
                </span>
            </div>
            <div style='display:flex; gap:16px; flex-wrap:wrap; margin-bottom:20px;'>
                <span style='background:#e3f2fd; color:#1565c0; padding:5px 14px;
                             border-radius:20px; font-size:12px; font-weight:700;'>
                    현재가 {r['price']:,.0f}
                </span>
                <span style='background:#f3e5f5; color:#6a1b9a; padding:5px 14px;
                             border-radius:20px; font-size:12px;'>
                    MA20 {r['ma20']:,.0f}
                </span>
                <span style='background:#e8f5e9; color:#2e7d32; padding:5px 14px;
                             border-radius:20px; font-size:12px;'>
                    MA60 {r['ma60']:,.0f}
                </span>
                <span style='background:#fff3e0; color:#e65100; padding:5px 14px;
                             border-radius:20px; font-size:12px;'>
                    RSI {r['rsi']:.1f}
                </span>
                <span style='background:#fafafa; color:#78909c; padding:5px 14px;
                             border-radius:20px; font-size:12px;'>
                    데이터 기준: {r['data_date']}
                </span>
            </div>
            <div style='font-size:13.5px; color:#1a2a45; line-height:2.0;
                        border-top:1px solid #f0f4ff; padding-top:16px;'>
                {analysis_html}
            </div>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang='ko'>
<head>
<meta charset='UTF-8'>
<link href='https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap' rel='stylesheet'>
<style>
  body {{ font-family:'Noto Sans KR',sans-serif; background:#f0f4fa;
          color:#1a2a45; margin:0; padding:24px; }}
  .container {{ max-width:740px; margin:0 auto; }}
  .header {{ background:linear-gradient(135deg,#0a3880,#1565c0,#1e88e5);
             border-radius:20px; padding:32px 36px; margin-bottom:28px;
             color:white; box-shadow:0 8px 30px rgba(10,56,128,0.25); }}
  .header h1 {{ margin:0 0 8px; font-size:24px; font-weight:900; letter-spacing:-0.5px; }}
  .header p  {{ margin:4px 0 0; opacity:0.85; font-size:13px; }}
  .footer {{ text-align:center; color:#b0bec5; font-size:11px;
             margin-top:24px; padding:16px;
             border-top:1px solid #dce6f5; }}
</style>
</head>
<body>
<div class='container'>
  <div class='header'>
    <h1>📈 매일 아침 주식 분석 리포트</h1>
    <p>발송 시각: {run_time} &nbsp;|&nbsp; 삼성전자 · SK하이닉스 · NVIDIA · Apple</p>
    <p style='margin-top:6px; font-size:11px; opacity:0.7;'>※ 데이터 출처: Yahoo Finance | AI 분석: Claude Haiku</p>
  </div>
  {cards}
  <div class='footer'>
    ※ 본 리포트는 AI 분석 참고 자료입니다. 투자 판단 및 손실 책임은 투자자 본인에게 있습니다.<br>
    <a href='https://stock-analysis-yhsctlbfdbbhzjbtbm8y6z.streamlit.app'
       style='color:#1565c0; text-decoration:none;'>🔗 상세 분석 사이트 바로가기</a>
  </div>
</div>
</body>
</html>"""

# ── 메인 실행 ──────────────────────────────────────────────────
def main():
    now_kst = datetime.now(KST)
    run_time = now_kst.strftime('%Y년 %m월 %d일 %H:%M (KST)')
    print(f"🚀 분석 시작: {run_time}")

    # 카카오 토큰 갱신
    kakao_token = refresh_kakao_token()
    print("✅ 카카오 토큰 처리 완료")

    stock_reports = []
    # 카카오용: 종목별 핵심 내용 포함 (실제 분석 내용)
    kakao_msg = f"📈 주식 분석 리포트\n{now_kst.strftime('%Y년 %m월 %d일 %H:%M')} KST\n{'─'*28}\n\n"

    for stock in STOCKS:
        print(f"📊 {stock['name']} 분석 중...")
        try:
            info = yf.Ticker(stock["ticker"])
            hist = info.history(period="3mo")

            # 데이터 신뢰도 검증
            valid, msg = validate_data(hist, stock['name'])
            if not valid:
                print(f"⚠️ {stock['name']} 데이터 검증 실패: {msg}")
                continue
            print(f"✅ {stock['name']} 데이터 검증: {msg}")

            price     = float(hist["Close"].iloc[-1])
            ma20      = float(hist["Close"].rolling(20).mean().dropna().iloc[-1])
            ma60      = float(hist["Close"].rolling(60).mean().dropna().iloc[-1]) if len(hist) >= 60 else ma20
            rsi       = float(calc_rsi(hist["Close"]))
            data_date = hist.index[-1].strftime('%Y-%m-%d')

            # 실시간 뉴스 가져오기
            news_items = []
            try:
                raw_news = info.news or []
                for n in raw_news[:8]:
                    c = n.get('content', {})
                    title = c.get('title', '')
                    pub   = c.get('pubDate', '')[:10] if c.get('pubDate') else ''
                    if title:
                        news_items.append(f"[{pub}] {title}")
            except:
                pass
            news_text = "\n".join(news_items) if news_items else "※ 현재 확인된 뉴스 없음"

            analysis = get_analysis(
                stock["ticker"], stock["name"], stock["market"],
                price, ma20, ma60, rsi, data_date, news_text
            )
            print(f"✅ {stock['name']} 분석 완료")

            stock_reports.append({
                "ticker": stock["ticker"], "name": stock["name"],
                "price": price, "ma20": ma20, "ma60": ma60, "rsi": rsi,
                "analysis": analysis, "data_date": data_date
            })

            # 카카오: 종목별 전체 분석 내용 포함 (핵심 섹션 위주)
            clean = clean_for_kakao(analysis)
            lines = [l.strip() for l in clean.split('\n') if l.strip()]
            # 앞 10줄 (결론 포함되도록)
            snippet = "\n".join(lines[:10])
            kakao_msg += (
                f"[ {stock['name']} ]  현재가: {price:,.0f}  |  RSI: {rsi:.1f}\n"
                f"데이터 기준: {data_date}\n"
                f"{snippet}\n"
                f"{'─'*28}\n\n"
            )

        except Exception as e:
            print(f"❌ {stock['name']} 오류: {e}")

    if not stock_reports:
        print("❌ 분석된 종목 없음")
        return

    # 이메일 발송
    try:
        html = make_html_report(stock_reports, run_time)
        send_email(
            f"📈 주식 분석 리포트 - {now_kst.strftime('%Y년 %m월 %d일')}",
            html
        )
        print("✅ 이메일 발송 완료")
    except Exception as e:
        print(f"❌ 이메일 오류: {e}")

    # 카카오 발송 — 종목별로 개별 메시지 전송 (9000자 제한 우회)
    header = f"📈 주식 분석 리포트 | {now_kst.strftime('%Y.%m.%d %H:%M')} KST\n{'─'*30}\n\n"
    for i, r in enumerate(stock_reports):
        try:
            clean = clean_for_kakao(r["analysis"])
            msg = (
                f"{'─'*30}\n"
                f"[{i+1}/4] {r['name']} ({r['ticker']})\n"
                f"현재가: {r['price']:,.0f}  |  RSI: {r['rsi']:.1f}  |  기준: {r['data_date']}\n"
                f"{'─'*30}\n\n"
                f"{clean}"
            )
            if i == 0:
                msg = header + msg
            result = send_kakao(msg, kakao_token)
            print(f"✅ 카카오 [{r['name']}] 발송: {result}")
            import time; time.sleep(1)  # 연속 발송 딜레이
        except Exception as e:
            print(f"❌ 카카오 [{r['name']}] 오류: {e}")

    print("🎉 모든 발송 완료!")

if __name__ == "__main__":
    main()
