import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import anthropic
import os
import json
import hashlib
import smtplib
from email.mime.text import MIMEText
from fpdf import FPDF
import tempfile
from datetime import datetime

# ── 설정 ──
ADMIN_ID = "whale"
ADMIN_PW_HASH = hashlib.sha256("stock2024".encode()).hexdigest()
ADMIN_EMAIL = "leero1126@gmail.com"
USERS_FILE = "users.json"
GMAIL_USER = "leero1126@gmail.com"
GMAIL_APP_PW = "xmpqsmeoexymwabm"

# ── 언어 ──
LANG = {
    "ko": {
        "title": "📈 주식 분석 프로그램",
        "login": "로그인", "register": "회원가입", "logout": "로그아웃",
        "id": "아이디", "pw": "비밀번호", "email": "이메일 (아이디로 사용)",
        "login_btn": "로그인", "register_btn": "가입 신청",
        "market": "시장 선택", "us": "🇺🇸 미국", "kr": "🇰🇷 한국",
        "input": "회사명 또는 티커를 입력하세요",
        "chart": "📊 차트", "signal": "🔍 기술적 신호",
        "ai": "🤖 AI 심층 분석", "ai_btn": "🔎 AI 분석 시작",
        "pdf_btn": "📄 PDF 저장", "loading": "데이터 불러오는 중...",
        "ai_loading": "AI가 분석 중입니다... (약 10~15초)",
        "welcome": "님 환영합니다!", "pending": "승인 대기 중입니다. 관리자 승인 후 이용 가능합니다.",
        "wrong_pw": "아이디 또는 비밀번호가 틀렸습니다.",
        "change_pw": "비밀번호 변경", "new_pw": "새 비밀번호", "confirm_pw": "비밀번호 확인",
        "pw_changed": "비밀번호가 변경되었습니다.", "pw_mismatch": "비밀번호가 일치하지 않습니다.",
        "admin_panel": "👑 관리자 패널", "pending_users": "승인 대기 회원",
        "approve": "✅ 승인", "reject": "❌ 거절",
        "no_pending": "대기 중인 회원이 없습니다.",
        "register_success": "가입 신청이 완료되었습니다. 관리자 승인을 기다려주세요.",
        "email_exists": "이미 등록된 이메일입니다.",
        "trend_up": "📈 추세: 상승 추세", "trend_down": "📉 추세: 하락 추세",
        "trend_side": "➡️ 추세: 횡보 / 전환 구간",
        "rsi_high": "🔴 RSI {}: 과매수 (매도 고려)",
        "rsi_low": "🟢 RSI {}: 과매도 (매수 고려)",
        "rsi_mid": "🔵 RSI {}: 중립 구간",
        "download": "📥 PDF 다운로드",
    },
    "en": {
        "title": "📈 Stock Analysis Program",
        "login": "Login", "register": "Sign Up", "logout": "Logout",
        "id": "Username", "pw": "Password", "email": "Email (used as username)",
        "login_btn": "Login", "register_btn": "Apply",
        "market": "Select Market", "us": "🇺🇸 US", "kr": "🇰🇷 Korea",
        "input": "Enter company name or ticker",
        "chart": "📊 Chart", "signal": "🔍 Technical Signals",
        "ai": "🤖 AI Deep Analysis", "ai_btn": "🔎 Start AI Analysis",
        "pdf_btn": "📄 Save PDF", "loading": "Loading data...",
        "ai_loading": "AI is analyzing... (about 10~15 sec)",
        "welcome": " Welcome!", "pending": "Pending approval. Please wait for admin approval.",
        "wrong_pw": "Incorrect username or password.",
        "change_pw": "Change Password", "new_pw": "New Password", "confirm_pw": "Confirm Password",
        "pw_changed": "Password has been changed.", "pw_mismatch": "Passwords do not match.",
        "admin_panel": "👑 Admin Panel", "pending_users": "Pending Users",
        "approve": "✅ Approve", "reject": "❌ Reject",
        "no_pending": "No pending users.",
        "register_success": "Registration submitted. Please wait for admin approval.",
        "email_exists": "Email already registered.",
        "trend_up": "📈 Trend: Uptrend", "trend_down": "📉 Trend: Downtrend",
        "trend_side": "➡️ Trend: Sideways",
        "rsi_high": "🔴 RSI {}: Overbought (Consider selling)",
        "rsi_low": "🟢 RSI {}: Oversold (Consider buying)",
        "rsi_mid": "🔵 RSI {}: Neutral",
        "download": "📥 Download PDF",
    }
}

def t(key):
    return LANG[st.session_state.get('lang', 'ko')].get(key, key)

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def send_email(to, subject, body):
    try:
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = GMAIL_USER
        msg['To'] = to
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PW)
            server.send_message(msg)
        return True
    except Exception as e:
        return False

def generate_pdf(ticker, analysis_text, price, ma20, ma60, rsi):
    pdf = FPDF()
    pdf.add_page()
    font_path = os.path.join(os.path.dirname(__file__), "NanumGothic.ttf")
    pdf.add_font("NanumGothic", "", font_path)
    pdf.set_font("NanumGothic", size=16)
    pdf.cell(0, 12, f"주식 분석 리포트 - {ticker}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("NanumGothic", size=10)
    pdf.cell(0, 8, f"날짜: {datetime.now().strftime('%Y-%m-%d %H:%M')}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("NanumGothic", size=12)
    pdf.cell(0, 8, "기술적 지표", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("NanumGothic", size=10)
    pdf.cell(0, 6, f"현재가: {price:.2f}  |  MA20: {ma20:.2f}  |  MA60: {ma60:.2f}  |  RSI: {rsi:.1f}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("NanumGothic", size=12)
    pdf.cell(0, 8, "AI 분석", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("NanumGothic", size=9)
    pdf.multi_cell(0, 5, analysis_text)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf.output(tmp.name)
    return tmp.name

def calc_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def get_ai_analysis(ticker, company, price, ma20, ma60, rsi, news_titles, market):
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    news_text = "\n".join([f"- {n}" for n in news_titles[:5]]) if news_titles else "관련 뉴스 없음"
    lang = st.session_state.get('lang', 'ko')
    lang_str = "한국어로" if lang == 'ko' else "in English"
    kr_market = market in ["🇰🇷 한국", "🇰🇷 Korea"]
    section1 = "1. 🌏 전일 미국 시장 분석 및 해당 종목 특별 이슈" if kr_market else "1. 🌏 주요 시장 영향 요소 및 해당 종목 특별 이슈"
    prompt = f"""
당신은 전문 주식 애널리스트입니다. {lang_str} 분석해주세요.
종목: {ticker} ({company})
현재가: {price:.2f} / MA20: {ma20:.2f} / MA60: {ma60:.2f} / RSI: {rsi:.1f}
최근 뉴스: {news_text}

아래 6가지를 분석해주세요:
{section1} (3~4문장)
2. 📢 시장 반응 및 여론 (2~3문장)
3. 📊 주가 등락 이유 (2~3문장)
4. 🔗 동반 상승/하락 예상 종목 (2~3문장)
5. 📅 당일 주식 전망 (3~4문장)
6. ✅ 최종 결론: 매수/매도/관망 중 하나 선택 (3~4문장)
"""
    message = client.messages.create(
        model="claude-haiku-4-5", max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

def name_to_ticker(query, market):
    korean_stocks = {
        "삼성전자": "005930.KS", "sk하이닉스": "000660.KS", "카카오": "035720.KS",
        "네이버": "035420.KS", "현대차": "005380.KS", "기아": "000270.KS",
        "셀트리온": "068270.KS", "kb금융": "105560.KS", "신한지주": "055550.KS",
        "삼성바이오로직스": "207940.KS", "포스코홀딩스": "005490.KS", "lg화학": "051910.KS",
        "현대모비스": "012330.KS", "sk텔레콤": "017670.KS", "lg에너지솔루션": "373220.KS",
        "카카오뱅크": "323410.KS", "하이브": "352820.KS", "크래프톤": "259960.KS",
    }
    if market in ["🇰🇷 한국", "🇰🇷 Korea"]:
        q = query.lower().replace(" ", "")
        for name, ticker in korean_stocks.items():
            if q in name or name in q:
                return ticker
        if not (query.endswith(".KS") or query.endswith(".KQ")):
            return query + ".KS"
        return query
    return query.upper()

def draw_chart(history, ticker):
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                        row_heights=[0.6, 0.2, 0.2], vertical_spacing=0.05)
    fig.add_trace(go.Scatter(x=history.index, y=history['Close'], name='Price', line=dict(color='blue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=history.index, y=history['MA20'], name='MA20', line=dict(color='orange')), row=1, col=1)
    fig.add_trace(go.Scatter(x=history.index, y=history['MA60'], name='MA60', line=dict(color='red')), row=1, col=1)
    fig.add_trace(go.Bar(x=history.index, y=history['Volume'], name='Volume', marker_color='gray'), row=2, col=1)
    fig.add_trace(go.Scatter(x=history.index, y=history['RSI'], name='RSI', line=dict(color='purple')), row=3, col=1)
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)
    fig.update_layout(height=700, title=f"{ticker} - Last 6 Months")
    return fig

def lang_toggle():
    cur = st.session_state.get('lang', 'ko')
    label = "🇺🇸 EN" if cur == 'ko' else "🇰🇷 KO"
    if st.button(label):
        st.session_state['lang'] = 'en' if cur == 'ko' else 'ko'
        st.rerun()

def login_page():
    col1, col2 = st.columns([5, 1])
    with col1:
        st.title(t("title"))
    with col2:
        lang_toggle()

    tab1, tab2 = st.tabs([t("login"), t("register")])

    with tab1:
        username = st.text_input(t("id"), key="login_id")
        password = st.text_input(t("pw"), type="password", key="login_pw")
        if st.button(t("login_btn")):
            if username == ADMIN_ID and hash_pw(password) == ADMIN_PW_HASH:
                st.session_state.update({'logged_in': True, 'username': username, 'is_admin': True})
                st.rerun()
            else:
                users = load_users()
                if username in users and users[username]['pw'] == hash_pw(password):
                    if users[username]['status'] == 'approved':
                        st.session_state.update({'logged_in': True, 'username': username, 'is_admin': False})
                        st.rerun()
                    else:
                        st.warning(t("pending"))
                else:
                    st.error(t("wrong_pw"))

    with tab2:
        email = st.text_input(t("email"), key="reg_email")
        pw1 = st.text_input(t("new_pw"), type="password", key="reg_pw1")
        pw2 = st.text_input(t("confirm_pw"), type="password", key="reg_pw2")
        if st.button(t("register_btn")):
            if not email:
                st.error("이메일을 입력하세요.")
            elif pw1 != pw2:
                st.error(t("pw_mismatch"))
            else:
                users = load_users()
                if email in users:
                    st.error(t("email_exists"))
                else:
                    users[email] = {'pw': hash_pw(pw1), 'status': 'pending',
                                    'created': datetime.now().strftime('%Y-%m-%d %H:%M')}
                    save_users(users)
                    send_email(ADMIN_EMAIL, "[주식앱] 신규 회원가입 승인 요청",
                               f"신규 가입 요청\n이메일: {email}\n\n앱에 로그인 후 관리자 패널에서 승인해주세요.")
                    st.success(t("register_success"))

def admin_panel():
    st.subheader(t("admin_panel"))
    users = load_users()
    pending = {k: v for k, v in users.items() if v['status'] == 'pending'}
    if pending:
        st.write(f"**{t('pending_users')} ({len(pending)}명)**")
        for email, info in pending.items():
            c1, c2, c3 = st.columns([3, 1, 1])
            c1.write(f"📧 {email}  ({info['created']})")
            if c2.button(t("approve"), key=f"ap_{email}"):
                users[email]['status'] = 'approved'
                save_users(users)
                send_email(email, "[주식앱] 가입 승인 완료", "가입이 승인되었습니다. 이제 로그인하실 수 있습니다.")
                st.rerun()
            if c3.button(t("reject"), key=f"rj_{email}"):
                del users[email]
                save_users(users)
                st.rerun()
    else:
        st.info(t("no_pending"))

def main_app():
    c1, c2, c3 = st.columns([4, 1, 1])
    with c1:
        st.title(t("title"))
    with c2:
        lang_toggle()
    with c3:
        if st.button(t("logout")):
            st.session_state['logged_in'] = False
            st.rerun()

    st.write(f"👤 **{st.session_state['username']}**{t('welcome')}")

    if st.session_state.get('is_admin'):
        with st.expander(t("admin_panel")):
            admin_panel()

    with st.expander(t("change_pw")):
        new_pw = st.text_input(t("new_pw"), type="password", key="cp_new")
        confirm = st.text_input(t("confirm_pw"), type="password", key="cp_confirm")
        if st.button(t("change_pw"), key="cp_btn"):
            if new_pw and new_pw == confirm:
                if not st.session_state.get('is_admin'):
                    users = load_users()
                    users[st.session_state['username']]['pw'] = hash_pw(new_pw)
                    save_users(users)
                st.success(t("pw_changed"))
            else:
                st.error(t("pw_mismatch"))

    st.divider()

    col_l, col_r = st.columns([1, 2])
    with col_l:
        market = st.radio(t("market"), [t("us"), t("kr")], horizontal=True)
    with col_r:
        st.info("예: AAPL, TSLA / 삼성전자, 카카오")

    default = "AAPL" if market == t("us") else "삼성전자"
    query = st.text_input(t("input"), value=default)

    if query:
        ticker = name_to_ticker(query, market)
        with st.spinner(t("loading")):
            stock = yf.Ticker(ticker)
            info = stock.info
            history = stock.history(period="6mo")

        if history.empty:
            st.error(f"'{query}' 데이터를 찾을 수 없습니다.")
            return

        currency = info.get('currency', 'USD')
        symbol = '₩' if currency == 'KRW' else '$'

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("회사명", info.get('longName', ticker))
        c2.metric("현재가", f"{symbol}{info.get('currentPrice', 'N/A'):,}")
        c3.metric("52주 최고가", f"{symbol}{info.get('fiftyTwoWeekHigh', 'N/A'):,}")
        c4.metric("52주 최저가", f"{symbol}{info.get('fiftyTwoWeekLow', 'N/A'):,}")

        st.divider()

        history['MA20'] = history['Close'].rolling(window=20).mean()
        history['MA60'] = history['Close'].rolling(window=60).mean()
        history['RSI'] = calc_rsi(history['Close'])

        price = float(history['Close'].dropna().iloc[-1])
        ma20 = float(history['MA20'].dropna().iloc[-1]) if not history['MA20'].dropna().empty else None
        ma60 = float(history['MA60'].dropna().iloc[-1]) if not history['MA60'].dropna().empty else None
        rsi = float(history['RSI'].dropna().iloc[-1]) if not history['RSI'].dropna().empty else 50.0

        st.subheader(t("chart"))
        st.plotly_chart(draw_chart(history, ticker), use_container_width=True)
        st.divider()

        st.subheader(t("signal"))
        c1, c2, c3 = st.columns(3)
        c1.metric("현재가", f"{symbol}{price:,.2f}")
        c2.metric("MA20", f"{symbol}{ma20:,.2f}" if ma20 else "N/A")
        c3.metric("MA60", f"{symbol}{ma60:,.2f}" if ma60 else "N/A")

        col1, col2 = st.columns(2)
        with col1:
            if ma20 and ma60 and price > ma20 > ma60:
                st.success(t("trend_up"))
            elif ma20 and ma60 and price < ma20 < ma60:
                st.error(t("trend_down"))
            else:
                st.warning(t("trend_side"))
        with col2:
            if rsi >= 70:
                st.error(t("rsi_high").format(f"{rsi:.1f}"))
            elif rsi <= 30:
                st.success(t("rsi_low").format(f"{rsi:.1f}"))
            else:
                st.info(t("rsi_mid").format(f"{rsi:.1f}"))

        st.divider()
        st.subheader(t("ai"))

        if st.button(t("ai_btn")):
            with st.spinner(t("ai_loading")):
                try:
                    news = stock.news or []
                    news_titles = [n.get('content', {}).get('title', '') for n in news if n.get('content', {}).get('title')]
                    company = info.get('longName', ticker)
                    analysis = get_ai_analysis(ticker, company, price, ma20 or 0, ma60 or 0, rsi, news_titles, market)
                    st.session_state['last_analysis'] = analysis
                    st.session_state['last_ticker'] = ticker
                    st.session_state['last_price'] = price
                    st.session_state['last_ma20'] = ma20 or 0
                    st.session_state['last_ma60'] = ma60 or 0
                    st.session_state['last_rsi'] = rsi
                except Exception as e:
                    st.error(f"오류: {e}")

        if st.session_state.get('last_analysis') and st.session_state.get('last_ticker') == ticker:
            st.write(st.session_state['last_analysis'])
            st.divider()
            pdf_path = generate_pdf(
                ticker, st.session_state['last_analysis'],
                st.session_state['last_price'], st.session_state['last_ma20'],
                st.session_state['last_ma60'], st.session_state['last_rsi']
            )
            with open(pdf_path, 'rb') as f:
                st.download_button(
                    label=t("pdf_btn"),
                    data=f.read(),
                    file_name=f"{ticker}_analysis_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )

# ── 시작 ──
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'lang' not in st.session_state:
    st.session_state['lang'] = 'ko'

if st.session_state['logged_in']:
    main_app()
else:
    login_page()