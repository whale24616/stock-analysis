"""
매수 문턱값 × 지표 가중치 프로파일 그리드서치.
5개 프로파일(현재/추세중심/평균회귀중심/거래량중심/균등) × 5개 문턱값을 in/out-sample로
나눠 평가하고, out-sample 성과가 좋으면서 in/out 괴리(과최적화 여부)가 작은 조합을 찾는다.
"""
from backtest import run_backtest, compute_metrics

PROFILES = {
    "현재(기본)":     {"trend": 0.278, "macd": 0.222, "rsi": 0.222, "bb": 0.167, "volume": 0.111},
    "추세중심":       {"trend": 0.40,  "macd": 0.30,  "rsi": 0.10,  "bb": 0.10,  "volume": 0.10},
    "평균회귀중심":   {"trend": 0.15,  "macd": 0.15,  "rsi": 0.35,  "bb": 0.25,  "volume": 0.10},
    "거래량중심":     {"trend": 0.25,  "macd": 0.20,  "rsi": 0.15,  "bb": 0.15,  "volume": 0.25},
    "균등":           {"trend": 0.20,  "macd": 0.20,  "rsi": 0.20,  "bb": 0.20,  "volume": 0.20},
}

THRESHOLDS = [25, 30, 40, 50, 60]


def fmt(m):
    if m is None:
        return "거래없음"
    return f"{m['trades']:>3}건 승률{m['win_rate']:>5.1f}% PF{m['profit_factor']:>5.2f} 기대값{m['expectancy']:>+6.2f}% 샤프{m['sharpe']:>5.2f}"


if __name__ == "__main__":
    results = []
    for name, weights in PROFILES.items():
        for th in THRESHOLDS:
            _, in_s, out_s = run_backtest(weights=weights, buy_threshold=th)
            m_in, m_out = compute_metrics(in_s), compute_metrics(out_s)
            gap = None
            if m_in and m_out:
                gap = abs(m_in["sharpe"] - m_out["sharpe"])
            results.append((name, th, m_in, m_out, gap))
            print(f"[{name:10}] 문턱{th:>3} | IN  {fmt(m_in)}")
            print(f"{'':14}       | OUT {fmt(m_out)}")

    # out-sample 거래 10건 이상 & 샤프 > 0.8 & in/out 괴리 작은 순으로 정렬
    valid = [r for r in results if r[3] and r[3]["trades"] >= 10 and r[3]["sharpe"] > 0.8 and r[4] is not None]
    valid.sort(key=lambda r: r[4])
    print("\n=== 안정적 후보 (out-sample 거래≥10, 샤프>0.8, in/out 괴리 작은 순) ===")
    for name, th, m_in, m_out, gap in valid[:8]:
        print(f"{name:10} 문턱{th:>3}  괴리{gap:.2f}  | IN {fmt(m_in)}  | OUT {fmt(m_out)}")
