import streamlit as st
st.set_page_config(page_title="주식 분석 프로그램", page_icon="📈", layout="wide")

import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import anthropic
import os, json, hashlib, smtplib, tempfile, base64, urllib.request
from email.mime.text import MIMEText
from fpdf import FPDF
from datetime import datetime

# ── 설정 ──────────────────────────────────────────────
ADMIN_ID      = "whale"
ADMIN_PW_HASH = hashlib.sha256("stock2024".encode()).hexdigest()
ADMIN_EMAIL   = "leero1126@gmail.com"
USERS_FILE    = "users.json"
GMAIL_USER    = "leero1126@gmail.com"
GMAIL_APP_PW  = "xmpqsmeoexymwabm"
FREE_LIMIT    = 5          # 무료 AI 분석 횟수
MONTHLY_FEE   = 5         # 월 구독료 ($)

# ── 다국어 ─────────────────────────────────────────────
LANG = {
    "ko": {
        "title": "주식 분석 프로그램", "subtitle": "AI 기반 실시간 주식 분석 플랫폼",
        "login": "로그인", "register": "회원가입", "logout": "로그아웃",
        "id": "아이디", "pw": "비밀번호", "email": "이메일 (아이디로 사용)",
        "login_btn": "로그인", "register_btn": "가입 신청",
        "market": "시장 선택", "us": "🇺🇸 미국", "kr": "🇰🇷 한국",
        "input": "회사명 또는 티커를 입력하세요",
        "chart": "📊 차트", "signal": "🔍 기술적 신호",
        "ai": "🤖 AI 심층 분석", "ai_btn": "🔎 AI 분석 시작",
        "pdf_btn": "📄 PDF 저장", "loading": "데이터 불러오는 중...",
        "ai_loading": "AI가 분석 중입니다... (약 10~15초)",
        "welcome": "님 환영합니다!", "pending": "승인 대기 중입니다.",
        "wrong_pw": "아이디 또는 비밀번호가 틀렸습니다.",
        "change_pw": "비밀번호 변경", "new_pw": "새 비밀번호", "confirm_pw": "비밀번호 확인",
        "pw_changed": "비밀번호가 변경되었습니다.", "pw_mismatch": "비밀번호가 일치하지 않습니다.",
        "admin_panel": "👑 관리자 패널", "pending_users": "승인 대기 회원",
        "approve": "✅ 승인", "reject": "❌ 거절", "no_pending": "대기 중인 회원이 없습니다.",
        "register_success": "가입 신청 완료! 관리자 승인을 기다려주세요.",
        "email_exists": "이미 등록된 이메일입니다.",
        "trend_up": "📈 추세: 상승 추세", "trend_down": "📉 추세: 하락 추세",
        "trend_side": "➡️ 추세: 횡보 / 전환 구간",
        "rsi_high": "🔴 RSI {}: 과매수 (매도 고려)",
        "rsi_low": "🟢 RSI {}: 과매도 (매수 고려)",
        "rsi_mid": "🔵 RSI {}: 중립 구간",
        "feature1": "실시간 주가 분석", "feature2": "AI 심층 분석", "feature3": "PDF 리포트",
        "feat1_desc": "한국/미국 주식 실시간 데이터", "feat2_desc": "Claude AI 기반 전문 분석", "feat3_desc": "분석 결과 PDF 저장",
        "sub_title": "💳 구독 플랜",
        "sub_free": "🎁 무료 체험", "sub_free_desc": "AI 분석 5회 무료",
        "sub_pro": "⭐ 프로 구독", "sub_pro_desc": "월 $5 · 무제한 AI 분석",
        "sub_status": "구독 현황", "sub_used": "사용한 무료 횟수",
        "sub_remain": "남은 무료 횟수", "sub_active": "✅ 구독 중 (무제한)",
        "pay_btn": "💳 월 $5 구독하기",
        "pay_success": "결제가 완료되었습니다! 구독이 활성화되었습니다.",
        "limit_msg": "무료 5회 분석을 모두 사용했습니다. 구독이 필요합니다.",
        "admin_sub": "구독 관리", "activate_sub": "✅ 구독 활성화", "deactivate_sub": "❌ 구독 해지",
        "reg_plan": "이용할 플랜을 선택하세요",
        "plan_free": "🎁 무료 체험 (5회 무료 후 구독)",
        "plan_pro": "⭐ 바로 구독 (월 $5)",
    },
    "en": {
        "title": "Stock Analysis Program", "subtitle": "AI-Powered Real-Time Stock Analysis Platform",
        "login": "Login", "register": "Sign Up", "logout": "Logout",
        "id": "Username", "pw": "Password", "email": "Email (used as ID)",
        "login_btn": "Login", "register_btn": "Apply",
        "market": "Select Market", "us": "🇺🇸 US", "kr": "🇰🇷 Korea",
        "input": "Enter company name or ticker",
        "chart": "📊 Chart", "signal": "🔍 Technical Signals",
        "ai": "🤖 AI Deep Analysis", "ai_btn": "🔎 Start AI Analysis",
        "pdf_btn": "📄 Save PDF", "loading": "Loading data...",
        "ai_loading": "AI is analyzing... (~10-15 sec)",
        "welcome": " Welcome!", "pending": "Pending approval.",
        "wrong_pw": "Incorrect username or password.",
        "change_pw": "Change Password", "new_pw": "New Password", "confirm_pw": "Confirm Password",
        "pw_changed": "Password changed.", "pw_mismatch": "Passwords do not match.",
        "admin_panel": "👑 Admin Panel", "pending_users": "Pending Users",
        "approve": "✅ Approve", "reject": "❌ Reject", "no_pending": "No pending users.",
        "register_success": "Registration submitted. Waiting for admin approval.",
        "email_exists": "Email already registered.",
        "trend_up": "📈 Trend: Uptrend", "trend_down": "📉 Trend: Downtrend",
        "trend_side": "➡️ Trend: Sideways",
        "rsi_high": "🔴 RSI {}: Overbought", "rsi_low": "🟢 RSI {}: Oversold", "rsi_mid": "🔵 RSI {}: Neutral",
        "feature1": "Real-time Analysis", "feature2": "AI Deep Analysis", "feature3": "PDF Report",
        "feat1_desc": "Korea/US stocks real-time", "feat2_desc": "Claude AI expert analysis", "feat3_desc": "Save as PDF",
        "sub_title": "💳 Subscription Plan",
        "sub_free": "🎁 Free Trial", "sub_free_desc": "5 free AI analyses",
        "sub_pro": "⭐ Pro Subscription", "sub_pro_desc": "$5/mo · Unlimited AI Analysis",
        "sub_status": "Subscription Status", "sub_used": "Free uses consumed",
        "sub_remain": "Free uses remaining", "sub_active": "✅ Active Subscription (Unlimited)",
        "pay_btn": "💳 Subscribe for $5/mo",
        "pay_success": "Payment complete! Subscription activated.",
        "limit_msg": "You've used all 5 free analyses. Subscription required.",
        "admin_sub": "Subscription Management", "activate_sub": "✅ Activate", "deactivate_sub": "❌ Deactivate",
        "reg_plan": "Select your plan after joining",
        "plan_free": "🎁 Free Trial (5 free, then subscribe)",
        "plan_pro": "⭐ Subscribe Now ($5/mo)",
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
        msg['Subject'] = subject; msg['From'] = GMAIL_USER; msg['To'] = to
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PW)
            server.send_message(msg)
        return True
    except:
        return False

# ── 스타일 ─────────────────────────────────────────────
def apply_style(with_bg=False):
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;500;600;700;800;900&family=Inter:wght@400;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Pretendard', 'Inter', sans-serif; }

    /* 전체 배경 — 미묘한 그라디언트 */
    .stApp { background: linear-gradient(160deg, #f0f4fb 0%, #eef2f9 100%) !important; }
    section[data-testid="stSidebar"] { background: #ffffff !important; }

    /* 텍스트 */
    h1 { color: #0a3272 !important; font-weight: 900 !important; letter-spacing:-0.5px; }
    h2, h3 { color: #1255a8 !important; font-weight: 700 !important; }
    p, label, div, span { color: #1a2a45 !important; }

    /* 버튼 내부 텍스트는 항상 흰색 */
    .stButton > button p,
    .stButton > button span,
    .stButton > button div,
    .stButton > button { color: #ffffff !important; }

    /* 메트릭 카드 — 더 세련되게 */
    [data-testid="metric-container"] {
        background: #ffffff !important;
        border: 1px solid #e0eaf8 !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: 0 4px 20px rgba(10,50,114,0.07) !important;
        transition: box-shadow 0.2s ease !important;
    }
    [data-testid="metric-container"]:hover {
        box-shadow: 0 8px 30px rgba(10,50,114,0.13) !important;
    }
    [data-testid="metric-container"] label {
        color: #6b8cc4 !important; font-size:0.73rem !important;
        text-transform:uppercase; letter-spacing:1.2px; font-weight:600 !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #0a1f4e !important; font-size:1.5rem !important; font-weight:800 !important;
    }

    /* 버튼 — 더 세련된 그라디언트 + 애니메이션 */
    .stButton > button {
        background: linear-gradient(135deg, #1255a8 0%, #0a3272 100%) !important;
        color: white !important; border: none !important;
        border-radius: 12px !important; padding: 11px 28px !important;
        font-weight: 700 !important; font-size: 0.93rem !important;
        letter-spacing: 0.3px !important;
        transition: all 0.25s cubic-bezier(0.4,0,0.2,1) !important;
        box-shadow: 0 4px 15px rgba(10,50,114,0.28) !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1976d2 0%, #1255a8 100%) !important;
        box-shadow: 0 8px 25px rgba(10,50,114,0.4) !important;
        transform: translateY(-2px) !important;
    }
    .stButton > button:active {
        transform: translateY(0px) !important;
        box-shadow: 0 3px 10px rgba(10,50,114,0.3) !important;
    }

    /* 입력란 */
    .stTextInput > div > div > input {
        background: #ffffff !important;
        border: 1.5px solid #c5d8f0 !important;
        border-radius: 12px !important;
        color: #0a1f4e !important;
        padding: 12px 18px !important;
        font-size: 0.95rem !important;
        box-shadow: 0 2px 8px rgba(10,50,114,0.05) !important;
        transition: all 0.2s ease !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #1255a8 !important;
        box-shadow: 0 0 0 3px rgba(18,85,168,0.12) !important;
        outline: none !important;
    }
    .stTextInput > div > div > input::placeholder { color: #a0b4cc !important; }
    .stTextInput label { color: #1a3a6e !important; font-weight: 600 !important; font-size:0.88rem !important; letter-spacing:0.3px; }

    /* 셀렉트박스 */
    .stSelectbox > div > div {
        background: #ffffff !important;
        border: 1.5px solid #c5d8f0 !important;
        border-radius: 12px !important;
    }

    /* 탭 — 더 깔끔하게 */
    .stTabs [data-baseweb="tab-list"] {
        background: #e4edf8 !important;
        border-radius: 14px !important; padding: 5px !important;
        border: 1px solid #cddaf0 !important;
        gap: 4px !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #4a6899 !important; border-radius:10px !important;
        font-weight:600 !important; padding:9px 22px !important;
        transition: all 0.2s ease !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1255a8, #0a3272) !important;
        color: white !important;
        box-shadow: 0 4px 14px rgba(10,50,114,0.3) !important;
    }
    .stTabs [aria-selected="true"] p { color: white !important; }

    /* 알림 박스 */
    .stSuccess { background: #e8f5e9 !important; border-left:4px solid #2e7d32 !important; border-radius:12px !important; }
    .stError   { background: #ffebee !important; border-left:4px solid #c62828 !important; border-radius:12px !important; }
    .stWarning { background: #fff8e1 !important; border-left:4px solid #ef6c00 !important; border-radius:12px !important; }
    .stInfo    { background: #e8f2fd !important; border-left:4px solid #1255a8 !important; border-radius:12px !important; }

    /* 익스팬더 */
    .streamlit-expanderHeader {
        background: #f0f5fc !important;
        border: 1px solid #d0e0f5 !important;
        border-radius: 12px !important;
        color: #1a3a6e !important;
        font-weight: 600 !important;
    }

    /* 구분선 */
    hr { border-color: #dce8f8 !important; }

    /* 라디오 */
    .stRadio label { color: #1a3a6e !important; font-weight:500 !important; }

    /* 스크롤바 */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #f0f4fb; }
    ::-webkit-scrollbar-thumb { background: #b0c8e8; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #1255a8; }

    #MainMenu {visibility:hidden;} footer {visibility:hidden;}
    </style>
    """, unsafe_allow_html=True)

def lang_toggle():
    cur = st.session_state.get('lang', 'ko')
    if st.button("🇺🇸 EN" if cur == 'ko' else "🇰🇷 KO", key="lang_btn"):
        st.session_state['lang'] = 'en' if cur == 'ko' else 'ko'
        st.rerun()

# ── 구독 관련 ────────────────────────────────────────────
def get_user_sub_info(username):
    if username == ADMIN_ID:
        return (9999, True)
    users = load_users()
    u = users.get(username, {})
    return (u.get('ai_count', 0), u.get('subscribed', False))

def can_use_ai(username):
    ai_count, subscribed = get_user_sub_info(username)
    return subscribed or ai_count < FREE_LIMIT

def increment_ai_count(username):
    if username == ADMIN_ID:
        return
    users = load_users()
    if username in users:
        users[username]['ai_count'] = users[username].get('ai_count', 0) + 1
        save_users(users)

def activate_subscription(username):
    users = load_users()
    if username in users:
        users[username]['subscribed'] = True
        users[username]['sub_date'] = datetime.now().strftime('%Y-%m-%d')
        save_users(users)

def deactivate_subscription(username):
    users = load_users()
    if username in users:
        users[username]['subscribed'] = False
        save_users(users)

# ── 결제 페이지 ─────────────────────────────────────────
def payment_page():
    ai_count, subscribed = get_user_sub_info(st.session_state['username'])
    remain = max(0, FREE_LIMIT - ai_count)

    st.markdown("""
    <style>
    .plan-card {
        background: rgba(255,255,255,0.88);
        border: 2px solid rgba(21,101,192,0.15);
        border-radius: 20px; padding: 32px 28px; text-align: center;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 30px rgba(21,101,192,0.1);
        transition: transform 0.2s, box-shadow 0.2s;
        height: 100%;
    }
    .plan-card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(21,101,192,0.18); }
    .plan-card.active { border-color: #1565c0; box-shadow: 0 8px 40px rgba(21,101,192,0.25); }
    .plan-price { font-size: 3rem; font-weight: 800; color: #0d47a1 !important; line-height:1; }
    .plan-period { font-size: 0.9rem; color: #5070a0 !important; margin-bottom:16px; }
    .plan-feature { padding: 7px 0; color: #2a4070 !important; font-size: 0.93rem; border-bottom:1px solid rgba(21,101,192,0.07); }
    .badge-free { background: #e8f5e9; color: #2e7d32 !important; padding:4px 14px; border-radius:20px; font-size:0.82rem; font-weight:700; }
    .badge-pro  { background: #e3f2fd; color: #0d47a1 !important; padding:4px 14px; border-radius:20px; font-size:0.82rem; font-weight:700; }
    .status-bar { background:rgba(255,255,255,0.85); border-radius:16px; padding:22px 28px; margin:16px 0;
                  border:1px solid rgba(21,101,192,0.12); box-shadow:0 4px 15px rgba(21,101,192,0.07); }
    .pay-card { background:rgba(255,255,255,0.88); border-radius:18px; padding:30px;
                border:1px solid rgba(21,101,192,0.15); box-shadow:0 4px 20px rgba(21,101,192,0.08); }
    .order-card { background:linear-gradient(135deg,rgba(21,101,192,0.06),rgba(13,71,161,0.09));
                  border-radius:16px; padding:24px; border:1px solid rgba(21,101,192,0.18); }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"<h2>{t('sub_title')}</h2>", unsafe_allow_html=True)

    # 현황 바
    if subscribed:
        sub_date = load_users().get(st.session_state['username'], {}).get('sub_date', '')
        st.markdown(f"""
        <div class="status-bar">
            <span style='font-size:1.3rem'>⭐</span>
            <span style='color:#0d47a1; font-weight:700; font-size:1.1rem;'> {t('sub_active')}</span>
            <span style='color:#5070a0; font-size:0.88rem; margin-left:14px;'>구독 시작: {sub_date}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        pct = min(int(ai_count / FREE_LIMIT * 100), 100)
        bar_color = "#00c853" if remain > 0 else "#d50000"
        st.markdown(f"""
        <div class="status-bar">
            <div style='display:flex; justify-content:space-between; margin-bottom:10px;'>
                <span style='color:#1a3a6e; font-weight:600; font-size:1rem;'>🎁 무료 AI 분석 현황</span>
                <span style='color:#1565c0; font-weight:700;'>{ai_count} / {FREE_LIMIT} 사용</span>
            </div>
            <div style='background:#e0e8f4; border-radius:10px; height:12px; overflow:hidden;'>
                <div style='width:{pct}%; background:{bar_color}; height:100%; border-radius:10px; transition:width 0.5s;'></div>
            </div>
            <div style='margin-top:10px; color:#5070a0; font-size:0.9rem;'>
                남은 무료 분석: <b style='color:#1565c0; font-size:1rem;'>{remain}회</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 플랜 카드
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown(f"""
        <div class="plan-card">
            <div style='margin-bottom:14px'><span class="badge-free">FREE</span></div>
            <div style='font-size:2.2rem; margin-bottom:8px;'>🎁</div>
            <h3 style='color:#1a3a6e !important; margin:6px 0 4px;'>{t('sub_free')}</h3>
            <div class="plan-price">$0</div>
            <div class="plan-period">영구 무료</div>
            <div class="plan-feature">✅ AI 분석 <b>5회</b> 무료</div>
            <div class="plan-feature">✅ 실시간 차트</div>
            <div class="plan-feature">✅ 기술적 신호 분석</div>
            <div class="plan-feature" style='color:#b0b8c8 !important;'>❌ PDF 리포트</div>
            <div class="plan-feature" style='color:#b0b8c8 !important; border:none;'>❌ 무제한 AI 분석</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        active_class = "active" if subscribed else ""
        st.markdown(f"""
        <div class="plan-card {active_class}">
            <div style='margin-bottom:14px'><span class="badge-pro">PRO</span></div>
            <div style='font-size:2.2rem; margin-bottom:8px;'>⭐</div>
            <h3 style='color:#1a3a6e !important; margin:6px 0 4px;'>{t('sub_pro')}</h3>
            <div class="plan-price">$5</div>
            <div class="plan-period">/ 월 · 언제든 해지 가능</div>
            <div class="plan-feature">✅ AI 분석 <b>무제한</b></div>
            <div class="plan-feature">✅ 실시간 차트</div>
            <div class="plan-feature">✅ 기술적 신호 분석</div>
            <div class="plan-feature">✅ PDF 리포트 저장</div>
            <div class="plan-feature" style='border:none;'>✅ 우선 고객 지원</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    if not subscribed:
        st.markdown("---")
        st.markdown("### 💳 결제 정보 입력")
        st.markdown("<br>", unsafe_allow_html=True)

        pay_col, order_col = st.columns([3, 2], gap="large")
        with pay_col:
            st.markdown('<div class="pay-card">', unsafe_allow_html=True)
            st.markdown("<b style='color:#0d47a1; font-size:1.05rem;'>💳 카드 정보</b>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            card_num  = st.text_input("카드 번호", placeholder="1234  5678  9012  3456", max_chars=19, key="card_num")
            c1, c2, c3 = st.columns(3)
            with c1: exp_m = st.text_input("만료 월", placeholder="MM", max_chars=2, key="exp_m")
            with c2: exp_y = st.text_input("만료 연도", placeholder="YY", max_chars=2, key="exp_y")
            with c3: cvc   = st.text_input("CVC", placeholder="•••", max_chars=3, type="password", key="cvc")
            card_name = st.text_input("카드 소유자 이름", placeholder="Hong Gil Dong", key="card_name")
            st.markdown("</div>", unsafe_allow_html=True)

        with order_col:
            st.markdown(f"""
            <div class="order-card">
                <div style='color:#0d47a1; font-weight:700; font-size:1rem; margin-bottom:18px;'>📋 주문 요약</div>
                <div style='display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid rgba(21,101,192,0.1);'>
                    <span style='color:#2a4070;'>주식 분석 Pro</span>
                    <span style='color:#1565c0; font-weight:600;'>$5.00</span>
                </div>
                <div style='display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid rgba(21,101,192,0.1);'>
                    <span style='color:#2a4070;'>세금</span>
                    <span style='color:#2a4070;'>$0.00</span>
                </div>
                <div style='display:flex; justify-content:space-between; padding:14px 0 0;'>
                    <span style='color:#0d47a1; font-weight:700; font-size:1.05rem;'>합계</span>
                    <span style='color:#0d47a1; font-weight:800; font-size:1.3rem;'>$5.00/월</span>
                </div>
                <div style='margin-top:20px; color:#5070a0; font-size:0.82rem; line-height:1.8;'>
                    🔒 256-bit SSL 암호화<br>
                    📅 매월 자동 갱신<br>
                    ❌ 언제든 해지 가능<br>
                    📧 영수증 이메일 발송
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💳  결제하고 Pro 구독 시작하기  →", use_container_width=True, key="pay_now"):
            if card_num and exp_m and exp_y and cvc and card_name:
                activate_subscription(st.session_state['username'])
                send_email(
                    st.session_state['username'],
                    "[주식 분석] 구독 결제 완료 ✅",
                    f"안녕하세요!\n\n주식 분석 Pro 구독이 성공적으로 활성화되었습니다.\n\n"
                    f"✅ 플랜: Pro (무제한 AI 분석)\n"
                    f"💰 금액: $5.00 / 월\n"
                    f"📅 시작일: {datetime.now().strftime('%Y-%m-%d')}\n\n감사합니다."
                )
                send_email(
                    ADMIN_EMAIL, "[주식앱] 신규 구독 결제",
                    f"신규 구독: {st.session_state['username']}\n시작일: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                )
                st.success(t("pay_success"))
                st.balloons()
                st.rerun()
            else:
                st.error("카드 정보를 모두 입력해주세요.")
        st.markdown("""
        <div style='text-align:center; color:#8090b0; font-size:0.8rem; margin-top:8px;'>
            🔒 카드 정보는 암호화되어 안전하게 처리됩니다.
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("<br>", unsafe_allow_html=True)
        _, c, _ = st.columns([2, 1, 2])
        with c:
            if st.button("❌ 구독 해지", key="unsub_btn"):
                deactivate_subscription(st.session_state['username'])
                st.warning("구독이 해지되었습니다.")
                st.rerun()

# ── 리포트 HTML 생성 (한글 100% 지원, 브라우저에서 PDF 저장) ─────
def generate_report_html(ticker, analysis_text, price, ma20, ma60, rsi):
    import re

    ma20_gap  = ((price - ma20) / ma20 * 100) if ma20 else 0
    ma60_gap  = ((price - ma60) / ma60 * 100) if ma60 else 0
    rsi_label = "과매수 🔴" if rsi >= 70 else ("과매도 🟢" if rsi <= 30 else "중립 🔵")
    now_str   = datetime.now().strftime('%Y년 %m월 %d일  %H:%M')

    # 마크다운 → HTML 변환
    def md_to_html(text):
        text = re.sub(r'~~(.*?)~~', r'\1', text)                        # 취소선 제거
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)            # 볼드
        text = re.sub(r'\*(.*?)\*',     r'<i>\1</i>', text)            # 이탤릭
        text = text.replace('&', '&amp;').replace('<b>', '<b>').replace('</b>', '</b>')
        return text

    # 섹션별로 분리해서 HTML 블록 생성
    section_starts = ['1.', '2.', '3.', '4.', '5.', '6.',
                      '✅', '📌', '📊', '📅', '📢', '🔗', '🌏']

    def is_heading(line):
        s = line.strip()
        if s.startswith('##'): return True
        if any(s.startswith(x) for x in section_starts): return True
        if len(s) > 2 and s[0].isdigit() and s[1] in '.）)': return True
        return False

    body_html = ""
    for line in analysis_text.split('\n'):
        stripped = line.strip()
        if not stripped:
            body_html += "<div style='height:10px'></div>\n"
        elif is_heading(stripped):
            clean = re.sub(r'^#+\s*', '', stripped)
            body_html += f"""
            <div class='section-title'>{md_to_html(clean)}</div>
            <div class='section-divider'></div>
            """
        else:
            body_html += f"<p>{md_to_html(stripped)}</p>\n"

    html = f"""<!DOCTYPE html>
<html lang='ko'>
<head>
<meta charset='UTF-8'>
<title>주식 분석 리포트 - {ticker}</title>
<link rel='preconnect' href='https://fonts.googleapis.com'>
<link href='https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap' rel='stylesheet'>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    font-family: 'Noto Sans KR', 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
    font-size: 11pt;
    color: #1a2a45;
    background: #fff;
    padding: 0;
  }}
  .page {{
    max-width: 780px;
    margin: 0 auto;
    padding: 40px 50px;
  }}
  .report-title {{
    font-size: 24pt;
    font-weight: 700;
    color: #0d47a1;
    margin-bottom: 6px;
  }}
  .report-meta {{
    font-size: 10pt;
    color: #555;
    margin-bottom: 4px;
  }}
  .header-line {{
    border: none;
    border-top: 2.5px solid #0d47a1;
    margin: 14px 0 18px 0;
  }}
  .indicator-table {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 22px;
    font-size: 10.5pt;
  }}
  .indicator-table td {{
    padding: 9px 14px;
    border: 1px solid #c8d8f0;
  }}
  .indicator-table tr:nth-child(odd)  {{ background: #eef4fc; }}
  .indicator-table tr:nth-child(even) {{ background: #f7faff; }}
  .indicator-table .label {{
    color: #1565c0;
    font-weight: 700;
    width: 90px;
  }}
  .section-title {{
    font-size: 13pt;
    font-weight: 700;
    color: #1565c0;
    margin: 22px 0 4px 0;
  }}
  .section-divider {{
    border-top: 1px solid #dce8f8;
    margin-bottom: 10px;
  }}
  p {{
    line-height: 1.85;
    margin-bottom: 8px;
    color: #1a2a45;
  }}
  .ai-section-title {{
    font-size: 13pt;
    font-weight: 700;
    color: #0d47a1;
    margin: 0 0 14px 0;
  }}
  .disclaimer {{
    margin-top: 30px;
    padding-top: 12px;
    border-top: 1px solid #ccc;
    font-size: 8.5pt;
    color: #888;
    line-height: 1.6;
  }}
  @media print {{
    body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
    .page {{ padding: 20px 30px; }}
    .no-print {{ display: none; }}
  }}
</style>
</head>
<body>
<div class='page'>

  <!-- 인쇄 안내 버튼 (화면에서만 보임) -->
  <div class='no-print' style='background:#e3f2fd; border:1px solid #90caf9;
       border-radius:10px; padding:12px 18px; margin-bottom:22px;
       font-size:10pt; color:#1565c0;'>
    💡 <b>PDF로 저장하려면:</b> 브라우저 메뉴 → 인쇄(Cmd+P) → '대상'을 <b>PDF로 저장</b> 선택
    &nbsp;&nbsp;
    <button onclick='window.print()' style='background:#1565c0; color:white;
      border:none; border-radius:6px; padding:6px 16px; cursor:pointer; font-size:10pt;'>
      🖨️ 인쇄 / PDF 저장
    </button>
  </div>

  <!-- 헤더 -->
  <div class='report-title'>📈 주식 분석 리포트</div>
  <div class='report-meta'>종목: <b>{ticker}</b> &nbsp;|&nbsp; 분석 시점: {now_str}</div>
  <hr class='header-line'>

  <!-- 기술적 지표 -->
  <div class='section-title'>■ 기술적 지표</div>
  <div class='section-divider'></div>
  <table class='indicator-table'>
    <tr>
      <td class='label'>현재가</td><td><b>{price:,.0f}원</b></td>
      <td class='label'>MA20</td><td>{ma20:,.0f} &nbsp;({ma20_gap:+.1f}%)</td>
    </tr>
    <tr>
      <td class='label'>MA60</td><td>{ma60:,.0f} &nbsp;({ma60_gap:+.1f}%)</td>
      <td class='label'>RSI(14)</td><td>{rsi:.1f} &nbsp;{rsi_label}</td>
    </tr>
  </table>

  <!-- AI 분석 -->
  <div class='ai-section-title'>■ AI 심층 분석</div>
  {body_html}

  <!-- 면책 고지 -->
  <div class='disclaimer'>
    ※ 본 리포트는 AI가 분석 시점({now_str})의 공개 정보를 바탕으로 생성한 참고 자료입니다.
    투자 판단 및 손실에 대한 책임은 투자자 본인에게 있습니다.
  </div>

</div>
</body>
</html>"""

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.html',
                                     mode='w', encoding='utf-8')
    tmp.write(html)
    tmp.close()
    return tmp.name

def calc_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def get_ai_analysis(ticker, company, price, ma20, ma60, rsi, news_titles, market):
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    news_text = "\n".join([f"- {n}" for n in news_titles[:8]]) if news_titles else "관련 뉴스 없음"
    lang = st.session_state.get('lang', 'ko')
    lang_str = "한국어로" if lang == 'ko' else "in English"
    kr_market = market in ["🇰🇷 한국", "🇰🇷 Korea"]

    # 기술적 지표 해석
    ma_status = "MA20 위 (단기 강세)" if price > ma20 else "MA20 아래 (단기 약세)"
    ma_cross  = "정배열 (MA20 > MA60, 강세)" if ma20 > ma60 else "역배열 (MA20 < MA60, 약세)"
    rsi_status = "과매수 구간" if rsi >= 70 else ("과매도 구간" if rsi <= 30 else "중립 구간")
    ma20_gap = ((price - ma20) / ma20 * 100) if ma20 else 0
    ma60_gap = ((price - ma60) / ma60 * 100) if ma60 else 0

    section1 = "1. 🌏 전일 미국 시장 분석 및 국내외 거시경제 환경" if kr_market else "1. 🌏 글로벌 시장 환경 및 거시경제 영향 요소"

    now_str = datetime.now().strftime('%Y년 %m월 %d일 %H시 %M분')
    prompt = f"""당신은 10년 경력의 주식 애널리스트입니다. {lang_str} 핵심 투자 판단 리포트를 작성하세요.

⚠️ 형식 규칙:
- **볼드** 사용 가능, ~~취소선~~ 절대 금지, ## 제목 금지
- 4개 항목 모두 완성 후 [END] 표시
- 장황한 설명 금지 — 투자자가 바로 행동할 수 있는 내용만

【분석 기준 시점】: {now_str}
【분석 종목】: {company} ({ticker})
【현재가】: {price:,.0f}
【MA20】: {ma20:,.0f} ({ma20_gap:+.1f}%) → {ma_status}
【MA60】: {ma60:,.0f} ({ma60_gap:+.1f}%) → {ma_cross}
【RSI(14)】: {rsi:.1f} → {rsi_status}
【최근 뉴스】:
{news_text}

아래 4개 항목을 순서대로 작성하세요:

1. 📰 최근 뉴스 & 여론
이 종목 관련 가장 최근 뉴스와 시장 여론을 **2문장으로만** 요약. 구체적 사실과 날짜 위주.

2. 📊 주가 흐름 분석
MA20/MA60/RSI 수치를 활용해 현재 추세와 위치를 3~4문장으로 분석. 수치 반드시 포함.

3. 🔗 연관 종목 동향
이 종목과 함께 움직이는 종목 3개와 현재 동향을 각 1문장씩.

4. ✅ 최종 투자 의견

아래 구조를 정확히 따라 작성하세요:

결론: "[매수/매도/관망(HOLD/BUY/SELL)]" — 한 줄 핵심 요약 (구체적 행동과 가격 포함)

근거:
- 근거 1 (수치 포함)
- 근거 2 (수치 포함)
- 근거 3 (수치 포함)

투자 가이드라인:
| 항목 | 수치 |
|------|------|
| 목표가 (3개월) | 구체적 가격 (+상승률%) |
| 손절가 | 구체적 가격 (-하락률%) |
| 추천 매수 시점 | 구체적 가격 조건 |
| 포지션 사이징 | 전체 자금의 X~Y% |
| 보유 기간 | X~Y개월 |

실행 방안:
1. 즉시 행동: 기존 보유자에 대한 구체적 조언
2. 대기 투자자: 진입 조건과 1차 매수 방법
3. 적극 공격자: 추가 진입 조건
4. 손실 관리: 손절 기준과 방법
"""
    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=5000,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

def name_to_ticker(query, market):
    korean_stocks = {
        # 반도체·IT
        "삼성전자":"005930.KS","sk하이닉스":"000660.KS","하이닉스":"000660.KS",
        "삼성sdi":"006400.KS","삼성전기":"009150.KS","lg이노텍":"011070.KS",
        # 인터넷·플랫폼
        "카카오":"035720.KS","네이버":"035420.KS","카카오뱅크":"323410.KS",
        "카카오페이":"377300.KS","크래프톤":"259960.KS","넥슨":"225570.KS",
        # 자동차
        "현대차":"005380.KS","현대자동차":"005380.KS","기아":"000270.KS","기아차":"000270.KS",
        "현대모비스":"012330.KS","한온시스템":"018880.KS",
        # 바이오·헬스
        "셀트리온":"068270.KS","삼성바이오로직스":"207940.KS","삼성바이오":"207940.KS",
        "유한양행":"000100.KS","한미약품":"128940.KS","에스티팜":"237690.KS",
        # 금융
        "kb금융":"105560.KS","신한지주":"055550.KS","하나금융지주":"086790.KS",
        "우리금융지주":"316140.KS","미래에셋증권":"006800.KS","삼성생명":"032830.KS",
        # 소재·에너지
        "포스코홀딩스":"005490.KS","포스코":"005490.KS","lg화학":"051910.KS",
        "lg에너지솔루션":"373220.KS","에코프로":"086520.KS","에코프로비엠":"247540.KS",
        # 통신
        "sk텔레콤":"017670.KS","kt":"030200.KS","lg유플러스":"032640.KS",
        # 엔터
        "하이브":"352820.KS","sm":"041510.KS","jyp":"035900.KS","yg":"122870.KS",
    }

    # 미국 주요 종목 한글→티커 매핑
    us_stocks = {
        # 빅테크
        "애플":"AAPL","엔비디아":"NVDA","마이크로소프트":"MSFT","구글":"GOOGL",
        "알파벳":"GOOGL","아마존":"AMZN","메타":"META","테슬라":"TSLA",
        "넷플릭스":"NFLX","인텔":"INTC","amd":"AMD","퀄컴":"QCOM",
        # AI·반도체
        "팔란티어":"PLTR","팔란티어테크":"PLTR","브로드컴":"AVGO","arm":"ARM",
        "슈퍼마이크로":"SMCI","어플라이드머티리얼즈":"AMAT","램리서치":"LRCX",
        # 금융
        "버크셔해서웨이":"BRK-B","jp모건":"JPM","뱅크오브아메리카":"BAC",
        "골드만삭스":"GS","비자":"V","마스터카드":"MA",
        # 소비재·유통
        "아마존":"AMZN","월마트":"WMT","코스트코":"COST","나이키":"NKE",
        # 헬스케어
        "존슨앤존슨":"JNJ","화이자":"PFE","모더나":"MRNA","일라이릴리":"LLY",
        # EV·에너지
        "리비안":"RIVN","루시드":"LCID","nio":"NIO","xpeng":"XPEV",
        # 기타 인기
        "스포티파이":"SPOT","유니티":"U","로블록스":"RBLX","스냅":"SNAP",
        "트위터":"X","코인베이스":"COIN","로빈후드":"HOOD","소파이":"SOFI",
        "스퀘어":"SQ","페이팔":"PYPL","줌":"ZM","도큐사인":"DOCU",
        "쇼피파이":"SHOP","에어비앤비":"ABNB","우버":"UBER","리프트":"LYFT",
        "스타벅스":"SBUX","맥도날드":"MCD","코카콜라":"KO","펩시":"PEP",
    }

    q = query.strip().lower().replace(" ", "").replace("-", "")

    if market in ["🇰🇷 한국", "🇰🇷 Korea"]:
        # 한글 이름 검색
        for name, ticker in korean_stocks.items():
            if q == name or q in name or name in q:
                return ticker
        # 티커 직접 입력 (.KS/.KQ 포함 여부)
        if not (query.upper().endswith(".KS") or query.upper().endswith(".KQ")):
            return query.upper() + ".KS"
        return query.upper()
    else:
        # 한글로 미국 종목 검색
        for name, ticker in us_stocks.items():
            if q == name or q in name or name in q:
                return ticker
        # 영문 티커 직접 입력
        return query.upper()

def draw_chart(history, ticker):
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                        row_heights=[0.6, 0.2, 0.2], vertical_spacing=0.04)
    fig.add_trace(go.Scatter(x=history.index, y=history['Close'], name='Price',
                             line=dict(color='#1565c0', width=2),
                             fill='tonexty', fillcolor='rgba(21,101,192,0.06)'), row=1, col=1)
    fig.add_trace(go.Scatter(x=history.index, y=history['MA20'], name='MA20',
                             line=dict(color='#ff6f00', width=1.5, dash='dot')), row=1, col=1)
    fig.add_trace(go.Scatter(x=history.index, y=history['MA60'], name='MA60',
                             line=dict(color='#c62828', width=1.5, dash='dash')), row=1, col=1)
    fig.add_trace(go.Bar(x=history.index, y=history['Volume'], name='Volume',
                         marker_color='rgba(21,101,192,0.35)'), row=2, col=1)
    fig.add_trace(go.Scatter(x=history.index, y=history['RSI'], name='RSI',
                             line=dict(color='#6a1b9a', width=1.5)), row=3, col=1)
    fig.add_hline(y=70, line_dash="dash", line_color="rgba(200,50,50,0.4)", row=3, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="rgba(30,150,30,0.4)", row=3, col=1)
    fig.update_layout(
        height=700,
        title=dict(text=f"  {ticker} — Last 6 Months", font=dict(color='#1a3a6e', size=15)),
        paper_bgcolor='rgba(255,255,255,0.88)', plot_bgcolor='rgba(240,246,255,0.8)',
        font=dict(color='#1a3a6e', family='Inter'),
        xaxis3=dict(gridcolor='rgba(21,101,192,0.08)', showgrid=True),
        yaxis=dict(gridcolor='rgba(21,101,192,0.08)', showgrid=True),
        yaxis2=dict(gridcolor='rgba(21,101,192,0.08)', showgrid=True),
        yaxis3=dict(gridcolor='rgba(21,101,192,0.08)', showgrid=True, range=[0,100]),
        legend=dict(bgcolor='rgba(255,255,255,0.85)', bordercolor='rgba(21,101,192,0.15)',
                    borderwidth=1, font=dict(size=11, color='#1a3a6e')),
        margin=dict(l=10, r=10, t=40, b=10),
    )
    return fig

# ── 로그인 페이지 ─────────────────────────────────────────
def login_page():
    apply_style()

    st.markdown("""
    <style>
    .login-glass {
        background: rgba(255,255,255,0.82);
        border: 1px solid rgba(21,101,192,0.15);
        border-radius: 22px; padding: 40px 36px;
        backdrop-filter: blur(22px);
        box-shadow: 0 20px 60px rgba(20,60,160,0.15);
        margin-bottom: 16px;
    }
    .left-hero {
        background: rgba(255,255,255,0.78);
        border: 1px solid rgba(21,101,192,0.12);
        border-radius: 22px; padding: 40px 32px;
        backdrop-filter: blur(18px);
        box-shadow: 0 16px 50px rgba(20,60,160,0.12);
    }
    .ticker-badge {
        display:inline-block; background:rgba(21,101,192,0.07);
        border:1px solid rgba(21,101,192,0.18); border-radius:20px;
        padding:5px 14px; margin:3px; font-size:0.82rem;
        color:#1565c0 !important; font-weight:500;
    }
    .feat-row { display:flex; align-items:center; padding:11px 0; border-bottom:1px solid rgba(21,101,192,0.07); }
    .feat-icon { font-size:1.5rem; margin-right:14px; min-width:32px; }
    .feat-title { color:#0d47a1 !important; font-weight:600; font-size:0.95rem; }
    .feat-desc  { color:#5070a0 !important; font-size:0.82rem; }
    .plan-mini {
        background:linear-gradient(135deg,rgba(21,101,192,0.06),rgba(13,71,161,0.09));
        border:1px solid rgba(21,101,192,0.18); border-radius:14px;
        padding:16px 20px; margin-top:22px;
        display:flex; justify-content:space-between; align-items:center;
    }
    </style>
    """, unsafe_allow_html=True)

    _, col_lang = st.columns([14, 1])
    with col_lang:
        lang_toggle()

    st.markdown("<br>", unsafe_allow_html=True)
    left_col, right_col = st.columns([1.3, 1], gap="large")

    with left_col:
        st.markdown(f"""
        <div class="left-hero">
            <div style="font-size:4rem; margin-bottom:10px;">📈</div>
            <h1 style="color:#0d47a1 !important; font-size:2.5rem !important; margin:0 0 8px; font-weight:800 !important;">
                {t('title')}
            </h1>
            <p style="color:#3060a0 !important; font-size:1.05rem; margin-bottom:22px; line-height:1.7;">
                {t('subtitle')}
            </p>
            <div style="margin-bottom:22px;">
                <span class="ticker-badge">🇺🇸 AAPL</span>
                <span class="ticker-badge">🇺🇸 TSLA</span>
                <span class="ticker-badge">🇺🇸 NVDA</span>
                <span class="ticker-badge">🇰🇷 삼성전자</span>
                <span class="ticker-badge">🇰🇷 SK하이닉스</span>
                <span class="ticker-badge">🇰🇷 카카오</span>
            </div>
            <div class="feat-row">
                <span class="feat-icon">📊</span>
                <div><div class="feat-title">{t('feature1')}</div><div class="feat-desc">{t('feat1_desc')}</div></div>
            </div>
            <div class="feat-row">
                <span class="feat-icon">🤖</span>
                <div><div class="feat-title">{t('feature2')}</div><div class="feat-desc">{t('feat2_desc')}</div></div>
            </div>
            <div class="feat-row" style="border:none;">
                <span class="feat-icon">📄</span>
                <div><div class="feat-title">{t('feature3')}</div><div class="feat-desc">{t('feat3_desc')}</div></div>
            </div>
            <div class="plan-mini">
                <div>
                    <span style="color:#1565c0; font-weight:700; font-size:0.95rem;">🎁 무료 체험</span>
                    <span style="color:#5070a0; font-size:0.82rem; margin-left:8px;">AI 분석 5회 무료</span>
                </div>
                <div>
                    <span style="color:#0d47a1; font-weight:800; font-size:1.2rem;">$5</span>
                    <span style="color:#5070a0; font-size:0.82rem;">/월 무제한</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right_col:
        st.markdown("<br>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs([f"🔐 {t('login')}", f"✏️ {t('register')}"])

        with tab1:
            st.markdown('<div class="login-glass">', unsafe_allow_html=True)
            st.markdown(f"<h3 style='color:#0d47a1 !important; margin-bottom:20px;'>🔐 {t('login')}</h3>", unsafe_allow_html=True)
            username = st.text_input(t("id"), key="login_id", placeholder="아이디 입력")
            password = st.text_input(t("pw"), type="password", key="login_pw", placeholder="비밀번호 입력")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(f"🔐 {t('login_btn')}", use_container_width=True, key="login_submit"):
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
            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="login-glass">', unsafe_allow_html=True)
            st.markdown(f"<h3 style='color:#0d47a1 !important; margin-bottom:20px;'>✏️ {t('register')}</h3>", unsafe_allow_html=True)
            email  = st.text_input(t("email"), key="reg_email", placeholder="example@email.com")
            pw1    = st.text_input(t("new_pw"),     type="password", key="reg_pw1", placeholder="비밀번호 입력")
            pw2    = st.text_input(t("confirm_pw"), type="password", key="reg_pw2", placeholder="비밀번호 확인")
            plan   = st.radio(t("reg_plan"), [t("plan_free"), t("plan_pro")], key="reg_plan_radio")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(f"✏️ {t('register_btn')}", use_container_width=True, key="reg_submit"):
                if not email:
                    st.error("이메일을 입력하세요.")
                elif pw1 != pw2:
                    st.error(t("pw_mismatch"))
                else:
                    users = load_users()
                    if email in users:
                        st.error(t("email_exists"))
                    else:
                        plan_key = 'pro' if t("plan_pro") in plan else 'free'
                        users[email] = {
                            'pw': hash_pw(pw1), 'status': 'pending',
                            'created': datetime.now().strftime('%Y-%m-%d %H:%M'),
                            'ai_count': 0, 'subscribed': False, 'plan': plan_key,
                        }
                        save_users(users)
                        plan_str = "Pro ($5/월)" if plan_key == 'pro' else "무료 체험"
                        send_email(ADMIN_EMAIL, "[주식앱] 신규 회원가입 승인 요청",
                                   f"신규 가입 요청\n이메일: {email}\n플랜: {plan_str}\n앱에서 승인해주세요.")
                        st.success(t("register_success"))
            st.markdown('</div>', unsafe_allow_html=True)

# ── 관리자 패널 ───────────────────────────────────────────
def admin_panel():
    users = load_users()
    pending  = {k: v for k, v in users.items() if v['status'] == 'pending'}
    approved = {k: v for k, v in users.items() if v['status'] == 'approved'}

    st.markdown(f"**{t('pending_users')}**")
    if pending:
        for email, info in pending.items():
            c1, c2, c3 = st.columns([4, 1, 1])
            c1.write(f"📧 {email} — {info.get('plan','free')} — {info.get('created','')}")
            if c2.button(t("approve"), key=f"ap_{email}"):
                users[email]['status'] = 'approved'
                if users[email].get('plan') == 'pro':
                    users[email]['subscribed'] = True
                    users[email]['sub_date'] = datetime.now().strftime('%Y-%m-%d')
                save_users(users)
                send_email(email, "[주식앱] 가입 승인 완료", "가입이 승인되었습니다. 앱에 접속해주세요.")
                st.rerun()
            if c3.button(t("reject"), key=f"rj_{email}"):
                del users[email]; save_users(users); st.rerun()
    else:
        st.info(t("no_pending"))

    st.markdown("---")
    st.markdown(f"**{t('admin_sub')}**")
    if approved:
        for email, info in approved.items():
            sub = info.get('subscribed', False)
            cnt = info.get('ai_count', 0)
            c1, c2 = st.columns([4, 1])
            c1.write(f"{'⭐' if sub else '🎁'} {email} | AI사용: {cnt}회 | {'구독중' if sub else '무료'}")
            if not sub:
                if c2.button(t("activate_sub"), key=f"sub_{email}"):
                    activate_subscription(email); st.rerun()
            else:
                if c2.button(t("deactivate_sub"), key=f"desub_{email}"):
                    deactivate_subscription(email); st.rerun()

# ── 메인 앱 ────────────────────────────────────────────────
def main_app():
    apply_style()

    # ── 헤더 배너 ──
    cur_lang = st.session_state.get('lang', 'ko')
    lang_label = "🇺🇸 EN" if cur_lang == 'ko' else "🇰🇷 KO"

    st.markdown(f"""
    <style>
    .main-header {{
        background: linear-gradient(135deg, #071e52 0%, #0a3272 45%, #1255a8 100%);
        border-radius: 18px; padding: 22px 32px; margin-bottom: 16px;
        box-shadow: 0 6px 28px rgba(7,30,82,0.35);
        display: flex; align-items: center; justify-content: space-between;
    }}
    .main-header .htitle {{
        font-size:1.9rem !important; font-weight:900 !important;
        color:#ffffff !important; letter-spacing:-0.5px; line-height:1.2;
        text-shadow:0 2px 10px rgba(0,0,0,0.5);
    }}
    .main-header .hsub {{
        color:rgba(210,228,255,0.95) !important; font-size:0.85rem; margin-top:5px;
    }}
    .hdr-btn-wrap {{ display:flex; gap:8px; align-items:center; }}
    .hdr-btn {{
        background: rgba(255,255,255,0.18);
        border: 1.5px solid rgba(255,255,255,0.5);
        border-radius: 10px; padding: 7px 16px;
        color: #ffffff !important; font-size: 0.82rem; font-weight: 700;
        cursor: pointer; white-space: nowrap;
        text-decoration: none; display: inline-block;
    }}
    .hdr-btn:hover {{ background: rgba(255,255,255,0.30); }}
    </style>
    <div class='main-header'>
        <div>
            <div class='htitle'>📈 {t('title')}</div>
            <div class='hsub'>{t('subtitle')}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 버튼 행 (헤더 아래 오른쪽 정렬)
    _, bcol = st.columns([6, 1])
    with bcol:
        lang_toggle()
        if st.button("🚪 로그아웃", key="logout_btn"):
            st.session_state['logged_in'] = False; st.rerun()

    ai_count, subscribed = get_user_sub_info(st.session_state['username'])
    remain     = max(0, FREE_LIMIT - ai_count)
    sub_badge  = "⭐ Pro 무제한" if subscribed else f"🎁 무료 {remain}/{FREE_LIMIT}회 남음"
    badge_color = "#0d47a1" if subscribed else "#2e7d32"
    st.markdown(
        f"<p style='color:#1a3a6e; margin-bottom:4px; font-size:0.95rem;'>"
        f"👤 <b>{st.session_state['username']}</b>{t('welcome')} &nbsp;"
        f"<span style='background:rgba(21,101,192,0.08); border:1px solid rgba(21,101,192,0.2); "
        f"border-radius:12px; padding:3px 12px; font-size:0.83rem; color:{badge_color} !important; font-weight:600;'>"
        f"{sub_badge}</span></p>",
        unsafe_allow_html=True
    )

    tab_main, tab_sub = st.tabs(["📊 주식 분석", "💳 구독 / 결제"])

    with tab_sub:
        payment_page()

    with tab_main:
        if st.session_state.get('is_admin'):
            with st.expander(t("admin_panel")):
                admin_panel()
        with st.expander(t("change_pw")):
            new_pw  = st.text_input(t("new_pw"),     type="password", key="cp_new")
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
        col_l, col_r = st.columns([1, 3])
        with col_l:
            market = st.radio(t("market"), [t("us"), t("kr")])
            st.markdown("<br>", unsafe_allow_html=True)
            query  = st.text_input(t("input"), value="AAPL" if market == t("us") else "삼성전자")

        with col_r:
            if query:
                ticker = name_to_ticker(query, market)
                with st.spinner(t("loading")):
                    stock   = yf.Ticker(ticker)
                    info    = stock.info
                    history = stock.history(period="6mo")

                if history.empty:
                    st.error(f"'{query}' 데이터를 찾을 수 없습니다.")
                    return

                currency = info.get('currency', 'USD')
                symbol   = '₩' if currency == 'KRW' else '$'

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("🏢 회사명",    info.get('longName', ticker))
                c2.metric("💰 현재가",    f"{symbol}{info.get('currentPrice', 'N/A'):,}")
                c3.metric("📈 52주 최고", f"{symbol}{info.get('fiftyTwoWeekHigh', 'N/A'):,}")
                c4.metric("📉 52주 최저", f"{symbol}{info.get('fiftyTwoWeekLow',  'N/A'):,}")

                history['MA20'] = history['Close'].rolling(window=20).mean()
                history['MA60'] = history['Close'].rolling(window=60).mean()
                history['RSI']  = calc_rsi(history['Close'])

                price = float(history['Close'].dropna().iloc[-1])
                ma20  = float(history['MA20'].dropna().iloc[-1]) if not history['MA20'].dropna().empty else 0.0
                ma60  = float(history['MA60'].dropna().iloc[-1]) if not history['MA60'].dropna().empty else 0.0
                rsi   = float(history['RSI'].dropna().iloc[-1])  if not history['RSI'].dropna().empty  else 50.0

                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader(t("chart"))
                st.plotly_chart(draw_chart(history, ticker), use_container_width=True)

                st.subheader(t("signal"))
                s1, s2, s3 = st.columns(3)
                s1.metric("현재가", f"{symbol}{price:,.2f}")
                s2.metric("MA20",  f"{symbol}{ma20:,.2f}" if ma20 else "N/A")
                s3.metric("MA60",  f"{symbol}{ma60:,.2f}" if ma60 else "N/A")
                sc1, sc2 = st.columns(2)
                with sc1:
                    if ma20 and ma60 and price > ma20 > ma60: st.success(t("trend_up"))
                    elif ma20 and ma60 and price < ma20 < ma60: st.error(t("trend_down"))
                    else: st.warning(t("trend_side"))
                with sc2:
                    if rsi >= 70:   st.error(t("rsi_high").format(f"{rsi:.1f}"))
                    elif rsi <= 30: st.success(t("rsi_low").format(f"{rsi:.1f}"))
                    else:           st.info(t("rsi_mid").format(f"{rsi:.1f}"))

                st.divider()
                st.subheader(t("ai"))

                ai_count2, subscribed2 = get_user_sub_info(st.session_state['username'])
                remain2 = max(0, FREE_LIMIT - ai_count2)

                if not subscribed2 and remain2 > 0:
                    st.info(f"🎁 무료 AI 분석 **{remain2}회** 남았습니다.")
                elif not subscribed2 and remain2 == 0:
                    st.warning(f"⚠️ {t('limit_msg')}")

                if can_use_ai(st.session_state['username']):
                    if st.button(t("ai_btn"), use_container_width=True):
                        with st.spinner(t("ai_loading")):
                            try:
                                news = stock.news or []
                                news_titles = [n.get('content', {}).get('title', '') for n in news
                                               if n.get('content', {}).get('title')]
                                company  = info.get('longName', ticker)
                                analysis = get_ai_analysis(ticker, company, price, ma20, ma60,
                                                           rsi, news_titles, market)
                                increment_ai_count(st.session_state['username'])
                                st.session_state.update({
                                    'last_analysis': analysis, 'last_ticker': ticker,
                                    'last_price': price, 'last_ma20': ma20,
                                    'last_ma60': ma60, 'last_rsi': rsi
                                })
                            except Exception as e:
                                st.error(f"오류: {e}")
                else:
                    st.markdown("""
                    <div style='background:rgba(255,200,0,0.08); border:1px solid rgba(255,160,0,0.3);
                                border-radius:12px; padding:20px; text-align:center;'>
                        <div style='font-size:1.5rem; margin-bottom:8px;'>🔒</div>
                        <div style='color:#8B4513 !important; font-weight:600; font-size:1rem;'>
                        무료 분석 5회를 모두 사용했습니다.</div>
                        <div style='color:#5070a0 !important; font-size:0.88rem; margin-top:6px;'>
                        <b>💳 구독 탭</b>에서 월 $5 Pro 구독을 시작하세요.</div>
                    </div>
                    """, unsafe_allow_html=True)

                if st.session_state.get('last_analysis') and st.session_state.get('last_ticker') == ticker:
                    st.markdown(f"""
                    <div style='background:rgba(255,255,255,0.88); border:1px solid rgba(21,101,192,0.15);
                                border-radius:16px; padding:28px; margin:16px 0;
                                box-shadow:0 8px 30px rgba(20,60,160,0.08);'>
                        <p style='color:#1a2a45 !important; line-height:1.9; white-space:pre-wrap; font-size:0.95rem;'>{st.session_state['last_analysis']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    html_path = generate_report_html(
                        ticker, st.session_state['last_analysis'],
                        st.session_state['last_price'], st.session_state['last_ma20'],
                        st.session_state['last_ma60'], st.session_state['last_rsi']
                    )
                    with open(html_path, 'r', encoding='utf-8') as f:
                        html_data = f.read()
                    st.download_button(
                        label="📄 리포트 저장 (HTML → 브라우저에서 PDF 변환)",
                        data=html_data.encode('utf-8'),
                        file_name=f"{ticker}_report_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
                        mime="text/html",
                        use_container_width=True
                    )
                    st.caption("💡 다운로드 후 파일을 열면 한글이 정상 표시됩니다. Cmd+P → PDF로 저장")

# ── 진입점 ─────────────────────────────────────────────────
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'lang' not in st.session_state:
    st.session_state['lang'] = 'ko'

if st.session_state['logged_in']:
    main_app()
else:
    login_page()
