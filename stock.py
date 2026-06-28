import yfinance as yf
import matplotlib.pyplot as plt

plt.rcParams['axes.unicode_minus'] = False

def calc_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

ticker = input("주식 티커를 입력하세요 (예: AAPL, TSLA): ")
stock = yf.Ticker(ticker)
info = stock.info

market_cap = info.get('marketCap', None)
market_cap_str = f"${market_cap:,}" if market_cap else "N/A"

print("\n=== 기본 정보 ===")
print(f"회사명: {info.get('longName', 'N/A')}")
print(f"현재가: ${info.get('currentPrice', 'N/A')}")
print(f"시가총액: {market_cap_str}")
print(f"52주 최고가: ${info.get('fiftyTwoWeekHigh', 'N/A')}")
print(f"52주 최저가: ${info.get('fiftyTwoWeekLow', 'N/A')}")

history = stock.history(period="6mo")
history['MA20'] = history['Close'].rolling(window=20).mean()
history['MA60'] = history['Close'].rolling(window=60).mean()
history['RSI'] = calc_rsi(history['Close'])

price = history['Close'].iloc[-1]
ma20  = history['MA20'].iloc[-1]
ma60  = history['MA60'].iloc[-1]
rsi   = history['RSI'].iloc[-1]

print("\n=== 기술적 분석 ===")
print(f"MA20: ${ma20:.2f}")
print(f"MA60: ${ma60:.2f}")
print(f"RSI:  {rsi:.1f}")

print("\n=== 신호 ===")
if price > ma20 > ma60:
    print("추세: 상승 추세 (Price > MA20 > MA60)")
elif price < ma20 < ma60:
    print("추세: 하락 추세 (Price < MA20 < MA60)")
else:
    print("추세: 횡보 / 전환 구간")

if rsi >= 70:
    print("RSI: 과매수 구간 (매도 고려)")
elif rsi <= 30:
    print("RSI: 과매도 구간 (매수 고려)")
else:
    print(f"RSI: 중립 구간 ({rsi:.1f})")

print("\nLoading chart...")

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [3, 1, 1]})

ax1.plot(history.index, history['Close'], color='blue', label='Price')
ax1.plot(history.index, history['MA20'], color='orange', label='MA20')
ax1.plot(history.index, history['MA60'], color='red', label='MA60')
ax1.set_title(f"{ticker} - Last 6 Months")
ax1.set_ylabel("Price (USD)")
ax1.legend()
ax1.grid(True)

ax2.bar(history.index, history['Volume'], color='gray', alpha=0.6)
ax2.set_ylabel("Volume")
ax2.grid(True)

ax3.plot(history.index, history['RSI'], color='purple')
ax3.axhline(70, color='red', linestyle='--', alpha=0.7)
ax3.axhline(30, color='green', linestyle='--', alpha=0.7)
ax3.set_ylabel("RSI")
ax3.set_xlabel("Date")
ax3.set_ylim(0, 100)
ax3.grid(True)

plt.tight_layout()
plt.show()