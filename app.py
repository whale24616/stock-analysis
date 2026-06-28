import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import anthropic
import os

USERS = {"admin": "1234", "whale": "stock2024"}

def login_page():
    st.title("🔐 주식 분석 프로그램")
    st.subheader("로그인")
    username = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")
    if st.button("로그인"):
        if username in USERS and USERS[username] == password:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.rerun()
        else:
            st.error("아이디 또는 비밀번호가 틀렸습니다.")

def name_to_ticker(query, market):
    korean_stocks = {
        "삼성전자": "005930.KS", "sk하이닉스": "000660.KS", "카카오": "035720.KS",
        "네이버": "035420.KS", "현대차": "005380.KS", "기아": "000270.KS",
        "셀트리온": "068270.KS", "kb금융": "105560.KS", "신한지주": "055550.KS",
        "삼성바이오로직스": "207940.KS", "포스코홀딩스": "005490.KS", "lg화학": "051910.KS",
        "현대모비스": "012330.KS", "sk텔레콤": "017670.KS", "lg에너지솔루션": "373220.KS",
        "카카오뱅크": "323410.KS", "하이브": "352820.KS", "크래프톤": "259960.KS",
        "삼성sdi": "006400.KS", "sk이노베이션": "096770.KS",
    }
    if market == "🇰🇷 한국":
        q = query.lower().replace(" ", "")
        for name, ticker in korean_stocks.items():
            if q in name or name in q:
                return ticker
        if not (query.endswith(".KS") or query.endswith(".KQ")):
            return query + ".KS"
        return query
    else:
        return query.upper()

def calc_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def get_ai_analysis(ticker, company, price, ma20, ma60, rsi, news_titles, market):
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    news_text = "\n".join([f"- {n}" for n in news_titles[:5]]) if news_titles else "관련 뉴스 없음"

    if market == "🇰🇷 한국":
        section1 = "1. 🌏 전일 미국 시장 분석 및 해당 종목 특별 이슈 (3~4문장: 전날 미국 증시 흐름이 오늘 이 종목에 미치는 영향 + 이 종목만의 특별한 이슈나 뉴스)"
    else:
        section1 = "1. 🌏 현재 시장에 영향을 미치는 주요 요소 및 해당 종목 특별 이슈 (3~4문장: 금리·환율·경제지표 등 거시적 요인 + 이 종목만의 특별한 이슈나 뉴스)"

    prompt = f"""
당신은 전문 주식 애널리스트입니다. 아래 데이터를 바탕으로 한국어로 분석해주세요.

종목: {ticker} ({company})
현재가: {price:.2f} / MA20: {ma20:.2f} / MA60: {ma60:.2f} / RSI: {rsi:.1f}
시장: {"한국 주식" if market == "🇰🇷 한국" else "미국 주식"}

최근 뉴스:
{news_text}

아래 6가지를 각각 분석해주세요:

{section1}

2. 📢 시장 반응 및 여론 (2~3문장)

3. 📊 주가 등락 이유 (2~3문장)

4. 🔗 동반 상승/하락 예상 종목 (2~3문장)

5. 📅 당일 주식 전망 (3~4문장: 오늘 이 종목의 상승·하락·정체 예상과 그 이유, 주목할 가격대)

6. ✅ 최종 결론 (3~4문장: 매수/매도/관망 중 하나를 명확히 선택하고 이유 설명)
"""
    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

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

def main_app():
    col_title, col_logout = st.columns([5, 1])
    with col_title:
        st.title("📈 주식 분석 프로그램")
    with col_logout:
        st.write("")
        if st.button("로그아웃"):
            st.session_state['logged_in'] = False
            st.rerun()

    st.write(f"👤 **{st.session_state['username']}**님 환영합니다!")
    st.divider()

    col_left, col_right = st.columns([1, 2])
    with col_left:
        market = st.radio("시장 선택", ["🇺🇸 미국", "🇰🇷 한국"], horizontal=True)
    with col_right:
        if market == "🇰🇷 한국":
            st.info("한국 주식: 회사명 입력 가능 (예: 삼성전자, 카카오, 현대차)")
        else:
            st.info("미국 주식: 티커 입력 (예: AAPL, TSLA, NVDA, MSFT)")

    default = "AAPL" if market == "🇺🇸 미국" else "삼성전자"
    query = st.text_input("회사명 또는 티커를 입력하세요", value=default)

    if query:
        ticker = name_to_ticker(query, market)
        with st.spinner("데이터 불러오는 중..."):
            stock = yf.Ticker(ticker)
            info = stock.info
            history = stock.history(period="6mo")

        if history.empty:
            st.error(f"'{query}' 데이터를 찾을 수 없습니다. 티커를 직접 입력해보세요.")
            return

        currency = info.get('currency', 'USD')
        symbol = '₩' if currency == 'KRW' else '$'

        # 기본 정보
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("회사명", info.get('longName', ticker))
        col2.metric("현재가", f"{symbol}{info.get('currentPrice', 'N/A'):,}")
        col3.metric("52주 최고가", f"{symbol}{info.get('fiftyTwoWeekHigh', 'N/A'):,}")
        col4.metric("52주 최저가", f"{symbol}{info.get('fiftyTwoWeekLow', 'N/A'):,}")

        st.divider()

        history['MA20'] = history['Close'].rolling(window=20).mean()
        history['MA60'] = history['Close'].rolling(window=60).mean()
        history['RSI'] = calc_rsi(history['Close'])

        price = history['Close'].iloc[-1]
        ma20  = history['MA20'].iloc[-1]
        ma60  = history['MA60'].iloc[-1]
        rsi   = history['RSI'].iloc[-1]

        # 차트 (기술적 신호 위)
        st.subheader("📊 차트")
        st.plotly_chart(draw_chart(history, ticker), use_container_width=True)

        st.divider()

        # 기술적 신호
        st.subheader("🔍 기술적 신호")
        c1, c2, c3 = st.columns(3)
        c1.metric("현재가", f"{symbol}{price:,.2f}" if price == price else "N/A")
        c2.metric("MA20", f"{symbol}{ma20:,.2f}" if ma20 == ma20 else "N/A")
        c3.metric("MA60", f"{symbol}{ma60:,.2f}" if ma60 == ma60 else "N/A")

        col1, col2 = st.columns(2)
        with col1:
            if price > ma20 > ma60:
                st.success("📈 추세: 상승 추세")
            elif price < ma20 < ma60:
                st.error("📉 추세: 하락 추세")
            else:
                st.warning("➡️ 추세: 횡보 / 전환 구간")
        with col2:
            if rsi >= 70:
                st.error(f"🔴 RSI {rsi:.1f}: 과매수 (매도 고려)")
            elif rsi <= 30:
                st.success(f"🟢 RSI {rsi:.1f}: 과매도 (매수 고려)")
            else:
                st.info(f"🔵 RSI {rsi:.1f}: 중립 구간")

        st.divider()

        # AI 분석
        st.subheader("🤖 AI 심층 분석")
        if st.button("🔎 AI 분석 시작"):
            with st.spinner("AI가 글로벌 데이터를 분석 중입니다... (약 10~15초)"):
                try:
                    news = stock.news or []
                    news_titles = [n.get('content', {}).get('title', '') for n in news if n.get('content', {}).get('title')]
                    company = info.get('longName', ticker)
                    analysis = get_ai_analysis(ticker, company, price, ma20, ma60, rsi, news_titles, market)
                    st.write(analysis)
                except Exception as e:
                    st.error(f"오류: {e}")

# ── 시작 ──
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    main_app()
else:
    login_page()