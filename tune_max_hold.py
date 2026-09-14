"""
보유기한(MAX_HOLD_DAYS) 그리드서치 — in-sample/out-of-sample을 나눠서
특정 값이 과거 구간에만 잘 맞는 과최적화인지 확인한다.
"""
from backtest import run_backtest, compute_metrics

CANDIDATES = [3, 5, 7, 10, 15, 20, 25, 30]


def fmt(m):
    if m is None:
        return f"{'거래없음':>44}"
    return (f"{m['trades']:>4}건 {m['win_rate']:>5.1f}% {m['profit_factor']:>5.2f} "
            f"{m['expectancy']:>+6.2f}% {m['sharpe']:>5.2f}")


if __name__ == "__main__":
    header = f"{'보유기한':>6} | {'IN-SAMPLE(거래/승률/손익비/기대값/샤프)':^36} | {'OUT-OF-SAMPLE':^36}"
    print(header)
    for days in CANDIDATES:
        _, in_s, out_s = run_backtest(max_hold_days=days)
        m_in, m_out = compute_metrics(in_s), compute_metrics(out_s)
        print(f"{days:>5}일 | {fmt(m_in):^36} | {fmt(m_out):^36}")
