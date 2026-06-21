"""
Generate synthetic weekly SOX-like data (2015-2026) that mimics real historical
cycle patterns: 2018 correction, 2020 COVID crash + recovery, 2021-22 bubble/bust,
2023-24 AI rally, 2025-26 consolidation.
"""

import numpy as np
import pandas as pd
from pathlib import Path

np.random.seed(42)

# Weekly dates 2015-01-02 to ~2026-06-20
dates = pd.date_range("2015-01-02", "2026-06-20", freq="W-FRI")
n = len(dates)

# ── SOX price path ──────────────────────────────────────────────────────────
# Piecewise trend + noise to capture major episodes
def make_sox(dates):
    t = np.arange(len(dates))
    price = np.zeros(n)
    price[0] = 600.0

    # regime parameters: (end_idx, weekly_drift, weekly_vol)
    regimes = [
        (52,   0.003, 0.025),   # 2015: moderate bull
        (104,  0.001, 0.030),   # 2016: choppy
        (156,  0.005, 0.020),   # 2017: strong bull
        (182, -0.010, 0.040),   # 2018 H1: correction
        (208,  0.004, 0.030),   # 2018 H2: recovery
        (214, -0.015, 0.050),   # Q4 2018: crash
        (270,  0.006, 0.025),   # 2019: recovery
        (276, -0.025, 0.070),   # Feb-Mar 2020: COVID crash
        (330,  0.012, 0.035),   # 2020 recovery
        (382,  0.010, 0.025),   # 2021: AI/semi boom
        (408, -0.015, 0.045),   # Q4 2021: peak/top
        (450, -0.008, 0.040),   # 2022: bear market
        (480,  0.008, 0.030),   # 2023 H1: recovery
        (530,  0.012, 0.025),   # 2023-24: AI rally
        (556,  0.005, 0.035),   # 2025: consolidation
        (n,   -0.002, 0.030),   # 2026: softening
    ]

    i = 1
    reg_start = 0
    for reg_end, drift, vol in regimes:
        while i < reg_end and i < n:
            ret = drift + vol * np.random.randn()
            price[i] = price[i-1] * (1 + ret)
            i += 1

    return price

sox = make_sox(dates)

# ── Derived features ─────────────────────────────────────────────────────────
sox_series = pd.Series(sox, index=dates)

ret_1w  = sox_series.pct_change(1)
ret_52w = sox_series.pct_change(52)
ma52    = sox_series.rolling(52).mean()

roll_m = ret_52w.rolling(260).mean()
roll_s = ret_52w.rolling(260).std()
price_momentum_z = ((ret_52w - roll_m) / roll_s).clip(-3, 3)

# ── P/E deviation: high during bull, mean-revert during bust ──────────────
# Synthetic P/E oscillates with price momentum + noise
pe_hist = 25.0
pe_raw  = 25 + 15 * np.tanh(price_momentum_z.fillna(0) * 0.8) + np.random.randn(n) * 3
pe_dev  = ((pe_raw - pe_hist) / pe_hist).clip(-0.5, 1.0)

# ── P/S deviation ─────────────────────────────────────────────────────────
ps_hist = 4.5
ps_raw  = 4.5 + 3.0 * np.tanh(price_momentum_z.fillna(0) * 0.7) + np.random.randn(n) * 0.5
ps_dev  = ((ps_raw - ps_hist) / ps_hist).clip(-0.5, 1.0)

# ── DIO: elevated in 2022 inventory glut, normal otherwise ────────────────
dio = np.full(n, 65.0)
# 2022 inventory glut: weeks ~370-430
dio[370:440] = 90 + np.random.randn(70) * 5
# 2018 build: weeks ~155-185
dio[155:185] = 75 + np.random.randn(30) * 4
dio_series = pd.Series(dio, index=dates)
# DIO Q/Q change (quarterly ≈ 13 weeks)
dio_qoq = dio_series.pct_change(13).clip(-0.5, 0.5).fillna(0)

# ── Capex surplus: Capex growth - Revenue growth ──────────────────────────
# High during boom phases
capex_surplus = 0.05 * np.tanh(price_momentum_z.fillna(0)) + np.random.randn(n) * 0.02
capex_surplus = pd.Series(capex_surplus, index=dates).clip(-0.3, 0.5)

# ── Sentiment (VIX proxy): inverse of fear ────────────────────────────────
# High during calm/bull, low during crash
vix_base = 18 - 10 * np.tanh(price_momentum_z.fillna(0) * 0.5) + np.abs(np.random.randn(n)) * 3
# Spike during crashes
vix_base[270:280] += 30   # COVID
vix_base[408:420] += 15   # 2022 bear
vix_series = pd.Series(vix_base, index=dates).clip(10, 85)
vix_m = vix_series.rolling(104).mean()
vix_s = vix_series.rolling(104).std()
sentiment_z = (-(vix_series - vix_m) / vix_s).clip(-3, 3)

# ── Assemble ─────────────────────────────────────────────────────────────
df = pd.DataFrame({
    "sox_close":        sox_series,
    "price_momentum_z": price_momentum_z,
    "pe_dev":           pd.Series(pe_dev, index=dates),
    "ps_dev":           pd.Series(ps_dev, index=dates),
    "capex_surplus":    capex_surplus,
    "dio":              dio_series,
    "dio_qoq":          dio_qoq,
    "sentiment_z":      sentiment_z,
}, index=dates)

df = df.dropna()
df.index.name = "date"

out = Path("/home/user/mycode/semi-overheat-model/data/raw/weekly_observations.csv")
out.parent.mkdir(parents=True, exist_ok=True)
df.round(4).to_csv(out)
print(f"Generated {len(df)} synthetic weekly rows → {out}")
print(df.tail(4))
