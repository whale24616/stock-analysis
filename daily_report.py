"""
매일 아침 7시 자동 실행 — 4개 종목 AI 분석 후 이메일 + 카카오 발송
"""
import os, json, smtplib, requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import yfinance as yf
import anthropic

# ── 설정 ──────────────────────────────────────────────────────
GMAIL_USER   = "leero1126@gmail.com"
GMAIL_APP_PW = "xmpqsmeoexymwabm"
SEND_TO      = "leero1126@gmail.com"   # 받을 이메일

ANTHROPIC_API_KEY    = os.environ.get("ANTHROPIC_API_KEY", "")
KAKAO_ACCESS_TOKEN   = os.environ.get("KAKAO_ACCESS_TOKEN", "")
KAKAO_REFRESH_TOKEN  = os.environ.get("KAKAO_REFRESH_TOKEN", "")
KAKAO_REST_API_KEY   = os.environ.get("KAKAO_REST_API_KEY", "")
KAKAO_CLIENT_SECRET  = os.environ.get("KAKAO_CLIENT_SECRET", "")

# ── 분석할 4개 종목 ────────────────────────────────────────────
STOCKS = [
    {"ticker": "005930.KS", "name": "삼성전자",  "market": "한국"},
    {"ticker": "000660.KS", "name": "SK하이닉스", "market": "한국"},
    {"ticker": "NVDA",      "name": "NVIDIA",    "market": "미국"},
    {"ticker": "AAPL",      "name": "Apple",     "market": "미국"},
]

# ── 카카오 토큰 갱신 ───────────────────────────────────────────
def refresh_kakao_token():
    res = requests.post("https://kauth.kakao.com/oauth/token", data={
        "grant_type":    "refresh_token",
        "client_id":     KAKAO_REST_API_KEY,
        "client_secret": KAKAO_CLIENT_SECRET,
        "refresh_token": KAKAO_REFRESH_TOKEN,
    })
    data = res.json()
    return data.get("access_token", KAKAO_ACCESS_TOKEN)

# ── 카카오 나에게 보내기 ────────────────────────────────────────
def send_kakao(text, access_token):
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    # 2000자 제한으로 자르기
    short_text = text[:1900] + "\n\n[전체 내용은 이메일 확인]" if len(text) > 1900 else text
    payload = {
        "template_object": json.dumps({
            "object_type": "text",
            "text": short_text,
            "link": {
                "web_url": "https://stock-analysis-yhsctlbfdbbhzjbtbm8y6z.streamlit.app",
                "mobile_web_url": "https://stock-analysis-yhsctlbfdbbhzjbtbm8y6z.streamlit.app"
            }
        })
    }
    res = requests.post(url, headers={"Authorization": f"Bearer {access_token}"}, data=payload)
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

# ── AI 분석 ────────────────────────────────────────────────────
def get_analysis(ticker, name, market, price, ma20, ma60, rsi):
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    now_str   = datetime.now().strftime('%Y년 %m월 %d일 %H시 %M분')
    ma20_gap  = ((price - ma20) / ma20 * 100) if ma20 else 0
    ma60_gap  = ((price - ma60) / ma60 * 100) if ma60 else 0
    rsi_label = "과매수" if rsi >= 70 else ("과매도" if rsi <= 30 else "중립")
    kr_market = market == "한국"
    section1  = "1. 🌏 전일 미국 시장 분석 및 국내외 거시경제 환경" if kr_market else "1. 🌏 글로벌 시장 환경 및 거시경제 영향 요소"

    prompt = f"""당신은 10년 경력의 주식 애널리스트입니다. 한국어로 분석 리포트를 작성하세요.

분석 기준 시점: {now_str}
종목: {name} ({ticker}) | 현재가: {price:,.0f} | MA20: {ma20:,.0f} ({ma20_gap:+.1f}%) | MA60: {ma60:,.0f} ({ma60_gap:+.1f}%) | RSI: {rsi:.1f} ({rsi_label})

작성 원칙:
- 각 항목: ① 결론(1~2문장) → ② 배경/이유(2~3문장) → ③ 세부내용(2~3문장)
- 쉬운 언어, 구체적 수치 포함
- 6개 항목 모두 완성 후 [END] 표시

{section1}
2. 📢 시장 반응 및 여론
3. 📊 주가 등락 이유
4. 🔗 함께 움직이는 연관 종목 3개
5. 📅 오늘~이번 주 전망 (지지선·저항선 가격 포함)
6. ✅ 최종 결론: 매수/매도/관망 (목표가·손절가 숫자로)
"""
    msg = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    return msg.content[0].text

# ── HTML 리포트 생성 ───────────────────────────────────────────
def make_html_report(stock_reports):
    now_str = datetime.now().strftime('%Y년 %m월 %d일 %H:%M')
    cards = ""
    for r in stock_reports:
        analysis_html = r["analysis"].replace("\n", "<br>")
        cards += f"""
        <div style='background:#fff; border:1px solid #dce8f8; border-radius:14px;
                    padding:28px; margin-bottom:30px;
                    box-shadow:0 4px 15px rgba(21,101,192,0.08);'>
            <div style='font-size:18px; font-weight:700; color:#0d47a1; margin-bottom:6px;'>
                📈 {r['name']} ({r['ticker']})
            </div>
            <div style='font-size:12px; color:#888; margin-bottom:16px;'>
                현재가: {r['price']:,.0f} &nbsp;|&nbsp;
                MA20: {r['ma20']:,.0f} &nbsp;|&nbsp;
                MA60: {r['ma60']:,.0f} &nbsp;|&nbsp;
                RSI: {r['rsi']:.1f}
            </div>
            <div style='font-size:13px; color:#1a2a45; line-height:1.9;'>
                {analysis_html}
            </div>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang='ko'>
<head>
<meta charset='UTF-8'>
<link href='https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap' rel='stylesheet'>
<style>
  body {{ font-family:'Noto Sans KR',sans-serif; background:#f5f7fa;
          color:#1a2a45; margin:0; padding:20px; }}
  .container {{ max-width:720px; margin:0 auto; }}
  .header {{ background:linear-gradient(135deg,#0d47a1,#1976d2);
             border-radius:16px; padding:28px 32px; margin-bottom:28px; color:white; }}
  .header h1 {{ margin:0; font-size:22px; }}
  .header p  {{ margin:6px 0 0; opacity:0.8; font-size:13px; }}
  .footer {{ text-align:center; color:#aaa; font-size:11px; margin-top:20px; }}
</style>
</head>
<body>
<div class='container'>
  <div class='header'>
    <h1>📈 매일 아침 주식 분석 리포트</h1>
    <p>분석 기준 시점: {now_str} &nbsp;|&nbsp; 삼성전자 · SK하이닉스 · NVIDIA · Apple</p>
  </div>
  {cards}
  <div class='footer'>
    ※ 본 리포트는 AI 분석 참고 자료입니다. 투자 판단 및 손실 책임은 투자자 본인에게 있습니다.
  </div>
</div>
</body>
</html>"""

# ── 메인 실행 ──────────────────────────────────────────────────
def main():
    print(f"🚀 분석 시작: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # 카카오 토큰 갱신
    kakao_token = refresh_kakao_token()
    print("✅ 카카오 토큰 갱신 완료")

    stock_reports = []
    kakao_summary = f"📈 주식 분석 리포트\n{datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}\n{'='*30}\n\n"

    for stock in STOCKS:
        print(f"📊 {stock['name']} 분석 중...")
        try:
            info    = yf.Ticker(stock["ticker"])
            hist    = info.history(period="3mo")
            if hist.empty:
                print(f"⚠️ {stock['name']} 데이터 없음")
                continue

            price = float(hist["Close"].iloc[-1])
            ma20  = float(hist["Close"].rolling(20).mean().dropna().iloc[-1])
            ma60  = float(hist["Close"].rolling(60).mean().dropna().iloc[-1]) if len(hist) >= 60 else ma20
            rsi   = float(calc_rsi(hist["Close"]))

            analysis = get_analysis(
                stock["ticker"], stock["name"], stock["market"],
                price, ma20, ma60, rsi
            )
            print(f"✅ {stock['name']} 분석 완료")

            stock_reports.append({
                "ticker": stock["ticker"], "name": stock["name"],
                "price": price, "ma20": ma20, "ma60": ma60, "rsi": rsi,
                "analysis": analysis
            })

            # 카카오용 요약 (종목별 핵심만)
            lines = analysis.split('\n')
            summary_lines = [l for l in lines if l.strip()][:8]
            kakao_summary += f"【{stock['name']}】현재가: {price:,.0f}\n"
            kakao_summary += "\n".join(summary_lines[:5]) + "\n\n"

        except Exception as e:
            print(f"❌ {stock['name']} 오류: {e}")

    if not stock_reports:
        print("❌ 분석된 종목 없음")
        return

    # 이메일 발송
    try:
        html = make_html_report(stock_reports)
        send_email(
            f"📈 주식 분석 리포트 - {datetime.now().strftime('%Y년 %m월 %d일')}",
            html
        )
        print("✅ 이메일 발송 완료")
    except Exception as e:
        print(f"❌ 이메일 오류: {e}")

    # 카카오 발송
    try:
        kakao_summary += "\n🔗 자세한 분석: stock-analysis-yhsctlbfdbbhzjbtbm8y6z.streamlit.app"
        result = send_kakao(kakao_summary, kakao_token)
        print(f"✅ 카카오 발송 완료: {result}")
    except Exception as e:
        print(f"❌ 카카오 오류: {e}")

    print("🎉 모든 발송 완료!")

if __name__ == "__main__":
    main()
