"""
Semiconductor Overheat Model
Uses realistic SOX-calibrated simulation (Yahoo Finance blocked in this env).
Historical SOX annualized return ~18%, vol ~28%, major drawdown events embedded.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import LinearSegmentedColormap
import warnings
warnings.filterwarnings("ignore")

# ── Parameters ───────────────────────────────────────────────────────────────
ZSCORE_WIN   = 252
RSI_WIN      = 14
OVERHEAT_Z   = 1.5
UNDERHEAT_Z  = -1.5
OUTPUT       = "semiconductor_overheat.png"

np.random.seed(42)

# ── Simulate realistic SOX price path (2015-01-02 to 2026-06-20) ─────────────
# SOX real stats: ~18% annual return, ~28% annual vol
# Key events encoded: 2018 selloff, 2020 COVID crash, 2021 bubble, 2022 bear, 2023-24 AI surge
dates = pd.bdate_range("2015-01-02", "2026-06-20")
n = len(dates)

ann_ret = 0.18
ann_vol = 0.28
dt = 1 / 252
mu  = ann_ret * dt
sig = ann_vol * np.sqrt(dt)

# Base GBM
raw_ret = np.random.normal(mu, sig, n)

# Regime overlays (index positions)
def date_idx(d):
    return int(np.searchsorted(dates, pd.Timestamp(d)))

regimes = [
    # (start, end, extra_drift_per_day, extra_vol_multiplier)
    ("2015-07-01", "2016-02-15", -0.003,  2.0),   # 2015-16 China/oil selloff
    ("2018-10-01", "2018-12-31", -0.005,  2.5),   # 2018 rate hike selloff
    ("2020-02-20", "2020-03-23", -0.010,  4.0),   # COVID crash
    ("2020-03-24", "2021-11-30",  0.003,  1.2),   # COVID recovery + boom
    ("2021-12-01", "2022-10-14", -0.004,  2.0),   # 2022 bear market
    ("2022-10-15", "2023-07-31",  0.004,  1.2),   # Recovery
    ("2023-08-01", "2024-12-31",  0.005,  1.0),   # AI / Nvidia boom
    ("2025-01-01", "2025-04-30", -0.003,  1.8),   # 2025 tariff uncertainty
    ("2025-05-01", "2026-06-20",  0.002,  1.2),   # Recovery
]

for start, end, drift, vol_mult in regimes:
    i0, i1 = date_idx(start), date_idx(end)
    raw_ret[i0:i1] = np.random.normal(mu + drift, sig * vol_mult, i1 - i0)

# Discrete shock events
for shock_date, shock_size in [
    ("2020-03-16", -0.14),
    ("2020-03-23", -0.08),
    ("2020-03-24",  0.12),
    ("2022-01-24",  0.06),
    ("2023-01-06",  0.07),
]:
    idx = date_idx(shock_date)
    if 0 <= idx < n:
        raw_ret[idx] = shock_size

# Build price series anchored to real SOX start (~650 in Jan 2015)
price = 650.0 * np.exp(np.cumsum(raw_ret))
df = pd.DataFrame({"close": price}, index=dates)

print(f"Simulated {len(df)} trading days  ({df.index[0].date()} → {df.index[-1].date()})")
print(f"  Start: {df['close'].iloc[0]:.0f}   End: {df['close'].iloc[-1]:.0f}")
print(f"  Peak:  {df['close'].max():.0f}   Trough: {df['close'].min():.0f}")

# ── Feature engineering ──────────────────────────────────────────────────────
df["log_ret"] = np.log(df["close"] / df["close"].shift(1))

roll = df["close"].rolling(ZSCORE_WIN)
df["z_score"] = (df["close"] - roll.mean()) / roll.std()

delta = df["close"].diff()
gain  = delta.clip(lower=0).rolling(RSI_WIN).mean()
loss  = (-delta.clip(upper=0)).rolling(RSI_WIN).mean()
df["rsi"] = 100 - 100 / (1 + gain / loss)

df["regime"] = "neutral"
df.loc[df["z_score"] >= OVERHEAT_Z,  "regime"] = "overheat"
df.loc[df["z_score"] <= UNDERHEAT_Z, "regime"] = "oversold"

rolling_max    = df["close"].cummax()
df["drawdown"] = (df["close"] - rolling_max) / rolling_max * 100

# ── Stats ────────────────────────────────────────────────────────────────────
total = df["regime"].notna().sum()
oh = (df["regime"] == "overheat").sum()
os_ = (df["regime"] == "oversold").sum()
print(f"\nRegime breakdown (Z-window={ZSCORE_WIN}d, threshold=±{OVERHEAT_Z}):")
print(f"  Overheat : {oh:>4d} days  ({oh/total*100:.1f}%)")
print(f"  Neutral  : {total-oh-os_:>4d} days  ({(total-oh-os_)/total*100:.1f}%)")
print(f"  Oversold : {os_:>4d} days  ({os_/total*100:.1f}%)")
print(f"  Latest Z : {df['z_score'].iloc[-1]:.2f}   RSI: {df['rsi'].iloc[-1]:.1f}")
print(f"  Latest   : {df['regime'].iloc[-1].upper()}")

# ── Plot ─────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(4, 1, figsize=(16, 18),
                         gridspec_kw={"height_ratios": [3, 1.2, 1.5, 1.2]},
                         facecolor="#0d1117")
fig.suptitle(
    "Semiconductor Sector (SOX) — Overheat / Oversold Model\n"
    "SOX-calibrated simulation · 2015–2026  |  Z-score window: 252 days",
    color="white", fontsize=15, fontweight="bold", y=0.99)

for ax in axes:
    ax.set_facecolor("#161b22")
    ax.tick_params(colors="#8b949e", labelsize=9)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    for sp in ax.spines.values():
        sp.set_edgecolor("#30363d")

dates_plot = df.index
close = df["close"]

# ── P1: Price ────────────────────────────────────────────────────────────────
ax1 = axes[0]
ax1.plot(dates_plot, close, color="#58a6ff", linewidth=1.1, zorder=3)
y_lo, y_hi = close.min() * 0.95, close.max() * 1.05

for regime, color in [("overheat", "#f85149"), ("oversold", "#3fb950")]:
    mask = df["regime"] == regime
    ax1.fill_between(dates_plot, y_lo, y_hi, where=mask,
                     color=color, alpha=0.22, zorder=1,
                     label=f"{regime.capitalize()} (Z{'≥' if regime=='overheat' else '≤'}{OVERHEAT_Z if regime=='overheat' else UNDERHEAT_Z})")

# Annotate key events
events = {
    "2018-12-24": "Rate hike\nselloff",
    "2020-03-23": "COVID\ncrash",
    "2021-11-19": "Peak\nbubble",
    "2022-10-14": "Bear\nbottom",
    "2023-10-26": "AI\nboom",
}
for d, label in events.items():
    ts = pd.Timestamp(d)
    if ts in df.index:
        ax1.annotate(label, xy=(ts, df.loc[ts, "close"]),
                     xytext=(0, 22), textcoords="offset points",
                     arrowprops=dict(arrowstyle="->", color="#8b949e", lw=0.8),
                     color="#e6edf3", fontsize=7.5, ha="center",
                     bbox=dict(boxstyle="round,pad=0.2", fc="#21262d", ec="#30363d", alpha=0.8))

ax1.set_ylim(y_lo, y_hi)
ax1.set_ylabel("Index Level", color="#8b949e")
ax1.set_title("Price History  (red shading = overheat · green shading = oversold)",
              color="#e6edf3", pad=6)
ax1.legend(loc="upper left", facecolor="#21262d", edgecolor="#30363d",
           labelcolor="#e6edf3", fontsize=9)

# ── P2: RSI ──────────────────────────────────────────────────────────────────
ax2 = axes[1]
ax2.plot(dates_plot, df["rsi"], color="#d2a8ff", linewidth=0.85)
ax2.axhline(70, color="#f85149", lw=0.8, ls="--", alpha=0.8, label="Overbought 70")
ax2.axhline(30, color="#3fb950", lw=0.8, ls="--", alpha=0.8, label="Oversold 30")
ax2.fill_between(dates_plot, 70, df["rsi"], where=(df["rsi"] >= 70), color="#f85149", alpha=0.35)
ax2.fill_between(dates_plot, 30, df["rsi"], where=(df["rsi"] <= 30), color="#3fb950", alpha=0.35)
ax2.set_ylim(0, 100)
ax2.set_yticks([20, 30, 50, 70, 80])
ax2.set_ylabel("RSI-14", color="#8b949e")
ax2.set_title("Relative Strength Index (14-day)", color="#e6edf3", pad=6)
ax2.legend(loc="lower left", facecolor="#21262d", edgecolor="#30363d",
           labelcolor="#e6edf3", fontsize=8)

# ── P3: Z-score ──────────────────────────────────────────────────────────────
ax3 = axes[2]
z = df["z_score"]
ax3.plot(dates_plot, z, color="#58a6ff", linewidth=0.75, alpha=0.7)
ax3.fill_between(dates_plot, OVERHEAT_Z, z, where=(z >= OVERHEAT_Z),
                 color="#f85149", alpha=0.55, label=f"Overheat (Z≥{OVERHEAT_Z})")
ax3.fill_between(dates_plot, UNDERHEAT_Z, z, where=(z <= UNDERHEAT_Z),
                 color="#3fb950", alpha=0.55, label=f"Oversold (Z≤{UNDERHEAT_Z})")
ax3.fill_between(dates_plot, 0, z,
                 where=((z > UNDERHEAT_Z) & (z < OVERHEAT_Z)),
                 color="#58a6ff", alpha=0.12)
ax3.axhline(OVERHEAT_Z,  color="#f85149", lw=0.8, ls="--")
ax3.axhline(UNDERHEAT_Z, color="#3fb950", lw=0.8, ls="--")
ax3.axhline(0,           color="#8b949e", lw=0.6, ls=":")
ax3.set_ylabel("Z-score", color="#8b949e")
ax3.set_title(f"Rolling {ZSCORE_WIN}-day Price Z-score  (deviation from 1-year mean)",
              color="#e6edf3", pad=6)
ax3.legend(loc="upper left", facecolor="#21262d", edgecolor="#30363d",
           labelcolor="#e6edf3", fontsize=9)

# ── P4: Drawdown ─────────────────────────────────────────────────────────────
ax4 = axes[3]
dd = df["drawdown"]
ax4.fill_between(dates_plot, dd, 0, color="#f85149", alpha=0.6)
ax4.plot(dates_plot, dd, color="#ff7b72", linewidth=0.7)
ax4.axhline(-20, color="#ffa657", lw=0.7, ls="--", alpha=0.7, label="-20% (correction)")
ax4.axhline(-40, color="#f85149", lw=0.7, ls="--", alpha=0.7, label="-40% (bear market)")
ax4.set_ylabel("Drawdown %", color="#8b949e")
ax4.set_title("Drawdown from Rolling All-Time High", color="#e6edf3", pad=6)
ax4.set_xlabel("Year", color="#8b949e")
ax4.legend(loc="lower left", facecolor="#21262d", edgecolor="#30363d",
           labelcolor="#e6edf3", fontsize=8)

for ax in axes:
    ax.set_xlim(dates_plot[0], dates_plot[-1])
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.grid(axis="y", color="#21262d", linewidth=0.5)

plt.tight_layout(rect=[0, 0, 1, 0.975])
plt.savefig(OUTPUT, dpi=150, bbox_inches="tight", facecolor="#0d1117")
print(f"\nChart saved → {OUTPUT}")
