"""
매일 아침 자동 실행 — 한국5+미국5 신호판(signals.py)을 계산해 이메일 + 카카오 발송
"""
import os, json, smtplib, requests, re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone, timedelta
import signals

# ── 설정 ──────────────────────────────────────────────────────
GMAIL_USER   = "leero1126@gmail.com"
GMAIL_APP_PW = "xmpqsmeoexymwabm"
SEND_TO      = "leero1126@gmail.com"

KAKAO_ACCESS_TOKEN   = os.environ.get("KAKAO_ACCESS_TOKEN", "").strip()
KAKAO_REFRESH_TOKEN  = os.environ.get("KAKAO_REFRESH_TOKEN", "").strip()
KAKAO_REST_API_KEY   = os.environ.get("KAKAO_REST_API_KEY", "").strip()
KAKAO_CLIENT_SECRET  = os.environ.get("KAKAO_CLIENT_SECRET", "").strip()

KST = timezone(timedelta(hours=9))

SIGNAL_EMOJI = {"매수": "🟢", "매도": "🔴", "관망": "⚪"}
SIGNAL_COLOR = {"매수": ("#2e7d32", "#e8f5e9"), "매도": ("#c62828", "#ffebee"), "관망": ("#78909c", "#f5f7fa")}

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

# ── HTML 리포트 생성 ───────────────────────────────────────────
def make_html_report(rows, run_time, stale_tickers):
    cards = ""
    for r in rows:
        fg, bg = SIGNAL_COLOR[r["signal"]]
        symbol = "₩" if r["market"] == "한국" else "$"
        stale_note = " ⚠️ 데이터 지연" if r["ticker"] in stale_tickers else ""
        cards += f"""
        <div style='background:#fff; border:1px solid #e0e8f5; border-radius:16px;
                    padding:24px; margin-bottom:20px;
                    box-shadow:0 4px 20px rgba(21,101,192,0.07);'>
            <div style='display:flex; align-items:center; justify-content:space-between; margin-bottom:14px; flex-wrap:wrap; gap:10px;'>
                <div>
                    <span style='font-size:19px; font-weight:800; color:#0d47a1;'>{r['name']}</span>
                    <span style='margin-left:8px; font-size:12px; color:#90a4ae;
                                 background:#f0f4ff; padding:3px 10px; border-radius:20px;'>{r['ticker']}</span>
                    <span style='margin-left:6px; font-size:12px; color:#607d8b;'>{r['sector']} · {r['market']}{stale_note}</span>
                </div>
                <span style='background:{bg}; color:{fg}; padding:6px 16px; border-radius:20px;
                             font-size:14px; font-weight:800;'>{r['signal']} {r['score']:+.1f}</span>
            </div>
            <div style='display:flex; gap:14px; flex-wrap:wrap;'>
                <span style='background:#e3f2fd; color:#1565c0; padding:5px 14px; border-radius:20px; font-size:12px; font-weight:700;'>현재가 {symbol}{r['price']:,.0f}</span>
                <span style='background:#ffebee; color:#c62828; padding:5px 14px; border-radius:20px; font-size:12px;'>손절가 {symbol}{r['stop_loss']:,.0f}</span>
                <span style='background:#e8f5e9; color:#2e7d32; padding:5px 14px; border-radius:20px; font-size:12px;'>목표가 {symbol}{r['take_profit']:,.0f}</span>
                <span style='background:#fff3e0; color:#e65100; padding:5px 14px; border-radius:20px; font-size:12px;'>RSI {r['rsi']:.0f}</span>
                <span style='background:#fafafa; color:#78909c; padding:5px 14px; border-radius:20px; font-size:12px;'>기준일 {r['data_date']}</span>
            </div>
        </div>
        """

    actionable = [r for r in rows if r["signal"] != "관망"]
    summary = (f"오늘 매수/매도 신호: {len(actionable)}건"
               if actionable else "오늘은 매수/매도 신호 없음 (전종목 관망)")

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
    <h1>📡 포트폴리오 신호판</h1>
    <p>발송 시각: {run_time} &nbsp;|&nbsp; {summary}</p>
    <p style='margin-top:6px; font-size:11px; opacity:0.7;'>※ 정량 스코어(ATR 기반 손절/익절, 백테스트 검증) | 투자 참고용, 투자 권유 아님</p>
  </div>
  {cards}
  <div class='footer'>
    ※ 본 리포트는 정량 스코어링 참고 자료입니다. 투자 판단 및 손실 책임은 투자자 본인에게 있습니다.<br>
    <a href='https://stock-analysis-yhsctlbfdbbhzjbtbm8y6z.streamlit.app'
       style='color:#1565c0; text-decoration:none;'>🔗 상세 신호판 바로가기</a>
  </div>
</div>
</body>
</html>"""

# ── 카카오 메시지 생성 ─────────────────────────────────────────
def make_kakao_message(rows, run_time):
    lines = [f"📡 포트폴리오 신호판 | {run_time}", "─" * 30]

    actionable = [r for r in rows if r["signal"] != "관망"]
    if actionable:
        lines.append("⚡ 오늘의 매수/매도 신호")
        for r in actionable:
            symbol = "₩" if r["market"] == "한국" else "$"
            lines.append(
                f"{SIGNAL_EMOJI[r['signal']]} {r['name']}({r['ticker']}) {r['signal']} {r['score']:+.1f}\n"
                f"   현재가 {symbol}{r['price']:,.0f} | 손절 {symbol}{r['stop_loss']:,.0f} | 목표 {symbol}{r['take_profit']:,.0f}"
            )
        lines.append("─" * 30)

    lines.append("전체 스코어 (높은 순)")
    for r in rows:
        lines.append(f"{SIGNAL_EMOJI[r['signal']]} {r['name']:10} {r['score']:>+6.1f}  {r['signal']}")

    return "\n".join(lines)

# ── 메인 실행 ──────────────────────────────────────────────────
def main():
    now = datetime.now(KST)
    run_time = now.strftime('%Y년 %m월 %d일 %H:%M (KST)')
    print(f"🚀 신호판 계산 시작: {run_time}")

    kakao_token = refresh_kakao_token()
    print("✅ 카카오 토큰 처리 완료")

    rows = signals.scan_all()
    if not rows:
        print("❌ 계산된 종목 없음")
        return
    print(f"✅ {len(rows)}종목 스코어 계산 완료")

    stale_tickers = []
    for r in rows:
        days_old = (now.date() - datetime.strptime(r["data_date"], "%Y-%m-%d").date()).days
        if days_old > 5:
            stale_tickers.append(r["ticker"])
            print(f"⚠️ {r['name']} 데이터가 {days_old}일 전 데이터 (지연 표시)")

    try:
        html = make_html_report(rows, run_time, stale_tickers)
        send_email(f"📡 포트폴리오 신호판 - {now.strftime('%Y년 %m월 %d일')}", html)
        print("✅ 이메일 발송 완료")
    except Exception as e:
        print(f"❌ 이메일 오류: {e}")

    try:
        kakao_msg = make_kakao_message(rows, run_time)
        result = send_kakao(kakao_msg, kakao_token)
        print(f"✅ 카카오 발송: {result}")
    except Exception as e:
        print(f"❌ 카카오 오류: {e}")

    print("🎉 모든 발송 완료!")

if __name__ == "__main__":
    main()
