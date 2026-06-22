"""
Semiconductor Sector Overheating Model
Signals: RSI · Price/SMA stretch · Rolling Z-score of returns · Composite Index

Data: Realistic synthetic prices seeded from known semi-sector patterns
      (NVDA ~10x 2020-2024 bull run, 2022 bear market, 2023-2024 AI boom).
      Replace `build_price_series()` with yf.download() when network access
      to query1/query2.finance.yahoo.com is enabled.
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

# ── Ticker universe ─────────────────────────────────────────────────────────────
SEMIS = {
    "NVDA": "NVIDIA",
    "AMD":  "AMD",
    "INTC": "Intel",
    "AVGO": "Broadcom",
    "QCOM": "Qualcomm",
    "MU":   "Micron",
    "AMAT": "Applied Materials",
    "KLAC": "KLA Corp",
    "LRCX": "Lam Research",
    "TXN":  "Texas Instruments",
}
ETF = "SOXX"

START = "2020-01-01"
END   = "2025-06-20"

# ── Realistic price generator ──────────────────────────────────────────────────

def build_price_series(dates: pd.DatetimeIndex,
                       start_price: float,
                       mu_phases: list[tuple],   # (end_date_str, annualised_drift)
                       sigma: float,
                       seed: int) -> pd.Series:
    """
    GBM simulation with piecewise drift to mimic observed semi-sector phases:
      2020      : recovery / bull
      2022      : rate-driven bear (-50 % sector peak-to-trough)
      2023-2024 : AI boom (NVDA +600 % from 2023 low)
      2025      : consolidation / mild pullback
    """
    rng = np.random.default_rng(seed)
    dt  = 1 / 252
    px  = [start_price]
    phase_dates = [(pd.Timestamp(d), mu) for d, mu in mu_phases]
    phase_idx   = 0

    for i in range(1, len(dates)):
        while (phase_idx < len(phase_dates) - 1 and
               dates[i] >= phase_dates[phase_idx + 1][0]):
            phase_idx += 1
        mu  = phase_dates[phase_idx][1]
        eps = rng.standard_normal()
        px.append(px[-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * eps))

    return pd.Series(px, index=dates)


PHASE_CONFIGS = {
    # ticker: (start_price, [(phase_end, annual_drift)], vol, seed)
    "NVDA": (14.0,  [("2021-12-01", 1.20), ("2022-10-01", -0.80),
                     ("2023-12-01", 2.80), ("2024-06-01", 1.40),
                     ("2025-06-20", -0.30)], 0.55, 1),
    "AMD":  (45.0,  [("2021-12-01", 0.95), ("2022-10-01", -0.70),
                     ("2023-12-01", 1.30), ("2024-06-01", 0.40),
                     ("2025-06-20", -0.20)], 0.50, 2),
    "INTC": (63.0,  [("2021-06-01", -0.10), ("2022-10-01", -0.55),
                     ("2023-12-01", 0.30), ("2024-06-01", -0.60),
                     ("2025-06-20", 0.10)], 0.35, 3),
    "AVGO": (325.0, [("2021-12-01", 0.60), ("2022-10-01", -0.40),
                     ("2023-12-01", 0.90), ("2024-06-01", 1.10),
                     ("2025-06-20", 0.15)], 0.38, 4),
    "QCOM": (90.0,  [("2021-12-01", 0.70), ("2022-10-01", -0.45),
                     ("2023-12-01", 0.55), ("2024-06-01", 0.25),
                     ("2025-06-20", -0.10)], 0.40, 5),
    "MU":   (55.0,  [("2021-12-01", 0.50), ("2022-10-01", -0.65),
                     ("2023-12-01", 1.10), ("2024-06-01", 0.60),
                     ("2025-06-20", -0.25)], 0.48, 6),
    "AMAT": (73.0,  [("2021-12-01", 0.90), ("2022-10-01", -0.50),
                     ("2023-12-01", 0.80), ("2024-06-01", 0.50),
                     ("2025-06-20", -0.15)], 0.42, 7),
    "KLAC": (210.0, [("2021-12-01", 0.85), ("2022-10-01", -0.45),
                     ("2023-12-01", 0.75), ("2024-06-01", 0.55),
                     ("2025-06-20", -0.10)], 0.40, 8),
    "LRCX": (380.0, [("2021-12-01", 0.80), ("2022-10-01", -0.55),
                     ("2023-12-01", 0.85), ("2024-06-01", 0.45),
                     ("2025-06-20", -0.15)], 0.42, 9),
    "TXN":  (135.0, [("2021-12-01", 0.30), ("2022-10-01", -0.25),
                     ("2023-12-01", 0.25), ("2024-06-01", 0.20),
                     ("2025-06-20",  0.05)], 0.28, 10),
    # SOXX ETF — basket-average profile
    ETF:    (290.0, [("2021-12-01", 0.75), ("2022-10-01", -0.55),
                     ("2023-12-01", 1.10), ("2024-06-01", 0.70),
                     ("2025-06-20", -0.20)], 0.40, 42),
}

print("Building realistic synthetic price series …")
dates  = pd.bdate_range(START, END)
prices = pd.DataFrame(index=dates)
for tk, (sp, phases, vol, seed) in PHASE_CONFIGS.items():
    prices[tk] = build_price_series(dates, sp, phases, vol, seed)

print(f"  {len(prices)} trading days  ({prices.index[0].date()} – {prices.index[-1].date()})")

# ── Signal functions ────────────────────────────────────────────────────────────

def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    d = series.diff()
    g = d.clip(lower=0).rolling(period).mean()
    l = (-d.clip(upper=0)).rolling(period).mean()
    return 100 - (100 / (1 + g / l.replace(0, np.nan)))


def overheating_score(px: pd.Series) -> pd.DataFrame:
    ret     = px.pct_change()
    rsi14   = rsi(px)
    sma200  = px.rolling(200).mean()
    stretch = (px / sma200 - 1) * 100
    z63     = (ret - ret.rolling(63).mean()) / ret.rolling(63).std()

    def pctrank(s):
        return s.rolling(252, min_periods=60).apply(
            lambda x: pd.Series(x).rank(pct=True).iloc[-1], raw=False
        )

    composite = (pctrank(rsi14) + pctrank(stretch) + pctrank(z63)) / 3

    return pd.DataFrame({
        "price": px, "rsi": rsi14, "stretch": stretch,
        "z_score": z63, "composite": composite,
    })


print("Computing overheating signals …")
etf_signals = overheating_score(prices[ETF])

stock_latest = {}
for tk in SEMIS:
    sig = overheating_score(prices[tk])
    stock_latest[tk] = {
        "name":      SEMIS[tk],
        "price":     sig["price"].iloc[-1],
        "rsi":       sig["rsi"].iloc[-1],
        "stretch":   sig["stretch"].iloc[-1],
        "composite": sig["composite"].iloc[-1],
    }

latest_df = pd.DataFrame(stock_latest).T
for col in ["price", "rsi", "stretch", "composite"]:
    latest_df[col] = pd.to_numeric(latest_df[col], errors="coerce")
latest_df = latest_df.sort_values("composite", ascending=False)

# ── Plot ────────────────────────────────────────────────────────────────────────
print("Generating charts …")
sns.set_theme(style="darkgrid")
fig = plt.figure(figsize=(20, 26))
fig.patch.set_facecolor("#0f1117")
gs  = fig.add_gridspec(4, 2, hspace=0.48, wspace=0.36)

AXIS_BG   = "#1a1d27"
TITLE_COL = "#e0e0e0"
LABEL_COL = "#aaaaaa"

def style_ax(ax, title=""):
    ax.set_facecolor(AXIS_BG)
    ax.tick_params(colors=LABEL_COL, labelsize=9)
    for sp in ax.spines.values():
        sp.set_edgecolor("#333344")
    if title:
        ax.set_title(title, color=TITLE_COL, fontsize=12, fontweight="bold", pad=8)
    ax.yaxis.label.set_color(LABEL_COL)
    ax.xaxis.label.set_color(LABEL_COL)

# ── (0) SOXX price + heat overlay ──────────────────────────────────────────────
ax0a = fig.add_subplot(gs[0, :])
style_ax(ax0a, f"SOXX Semiconductor ETF — Price & Composite Overheating Index  ({START} – {END})")

ax0a.plot(etf_signals.index, etf_signals["price"], color="#4fc3f7", lw=1.4, label="SOXX Price")
ax0a.set_ylabel("Price (USD)", color="#4fc3f7")
ax0a.tick_params(axis="y", labelcolor="#4fc3f7")

ax0b = ax0a.twinx()
ax0b.set_facecolor(AXIS_BG)
comp = etf_signals["composite"].fillna(0)

for i in range(len(etf_signals) - 1):
    ax0b.axvspan(etf_signals.index[i], etf_signals.index[i + 1],
                 alpha=0.22, color=plt.cm.RdYlGn_r(comp.iloc[i]), lw=0)

ax0b.plot(etf_signals.index, comp, color="#ff7043", lw=1.3, alpha=0.9, label="Composite Score")
ax0b.axhline(0.75, color="#ef5350", ls="--", lw=0.9, alpha=0.75, label="Overheating ≥ 0.75")
ax0b.axhline(0.25, color="#66bb6a", ls="--", lw=0.9, alpha=0.75, label="Oversold ≤ 0.25")
ax0b.set_ylim(0, 1)
ax0b.set_ylabel("Composite Overheating Index", color="#ff7043")
ax0b.tick_params(axis="y", labelcolor="#ff7043")
ax0b.legend(loc="upper left", fontsize=8, facecolor=AXIS_BG, labelcolor=LABEL_COL)
ax0a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
ax0a.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
plt.setp(ax0a.xaxis.get_majorticklabels(), rotation=30, ha="right")

# ── (1) SOXX RSI ────────────────────────────────────────────────────────────────
ax1 = fig.add_subplot(gs[1, 0])
style_ax(ax1, "SOXX — RSI (14-day)")
ax1.plot(etf_signals.index, etf_signals["rsi"], color="#ba68c8", lw=1.2)
ax1.fill_between(etf_signals.index, etf_signals["rsi"], 70,
                 where=(etf_signals["rsi"] >= 70), alpha=0.25, color="#ef5350")
ax1.fill_between(etf_signals.index, etf_signals["rsi"], 30,
                 where=(etf_signals["rsi"] <= 30), alpha=0.25, color="#66bb6a")
ax1.axhline(70, color="#ef5350", ls="--", lw=0.8, label="Overbought 70")
ax1.axhline(30, color="#66bb6a", ls="--", lw=0.8, label="Oversold 30")
ax1.set_ylim(0, 100); ax1.set_ylabel("RSI")
ax1.legend(fontsize=8, facecolor=AXIS_BG, labelcolor=LABEL_COL)
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=30, ha="right")

# ── (2) % above 200-day SMA ─────────────────────────────────────────────────────
ax2 = fig.add_subplot(gs[1, 1])
style_ax(ax2, "SOXX — % Above 200-Day SMA")
st = etf_signals["stretch"].dropna()
ax2.fill_between(st.index, st, 0, where=(st >= 0), alpha=0.4, color="#ef5350", label="Above SMA")
ax2.fill_between(st.index, st, 0, where=(st < 0),  alpha=0.4, color="#66bb6a", label="Below SMA")
ax2.plot(st.index, st, color="#ffca28", lw=0.9, alpha=0.8)
ax2.axhline(0, color=LABEL_COL, lw=0.7)
ax2.set_ylabel("% deviation")
ax2.legend(fontsize=8, facecolor=AXIS_BG, labelcolor=LABEL_COL)
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=30, ha="right")

# ── (3) Per-stock heatmap ────────────────────────────────────────────────────────
ax3 = fig.add_subplot(gs[2, 0])
style_ax(ax3, f"Latest Composite Overheating Score  ({END})")
scores = latest_df["composite"].values.reshape(-1, 1)
ylabels = [f"{tk}  {SEMIS[tk]}" for tk in latest_df.index]
im = ax3.imshow(scores, cmap="RdYlGn_r", vmin=0, vmax=1, aspect="auto")
ax3.set_yticks(range(len(ylabels)))
ax3.set_yticklabels(ylabels, fontsize=9, color=TITLE_COL)
ax3.set_xticks([])
for i, v in enumerate(latest_df["composite"].values):
    ax3.text(0, i, f"{v:.2f}", ha="center", va="center", fontsize=11, fontweight="bold",
             color="black" if 0.3 < v < 0.75 else "white")
plt.colorbar(im, ax=ax3, label="0 = cold  |  1 = overheated")

# ── (4) Scatter RSI vs Stretch ──────────────────────────────────────────────────
ax4 = fig.add_subplot(gs[2, 1])
style_ax(ax4, "RSI vs % Above 200-Day SMA — Current Snapshot")
sc = ax4.scatter(
    latest_df["stretch"], latest_df["rsi"],
    c=latest_df["composite"], cmap="RdYlGn_r", vmin=0, vmax=1,
    s=140, edgecolors="white", linewidths=0.6, zorder=3
)
for _, row in latest_df.iterrows():
    ax4.annotate(row.name, (row["stretch"], row["rsi"]),
                 xytext=(5, 4), textcoords="offset points", fontsize=9, color=TITLE_COL)
ax4.axhline(70, color="#ef5350", ls="--", lw=0.8, alpha=0.6)
ax4.axhline(30, color="#66bb6a", ls="--", lw=0.8, alpha=0.6)
ax4.axvline(0,  color=LABEL_COL,  ls="--", lw=0.8, alpha=0.5)
ax4.set_xlabel("% Above 200-Day SMA"); ax4.set_ylabel("RSI (14-day)")
plt.colorbar(sc, ax=ax4, label="Composite Score")

# ── (5) Ranked bar chart ─────────────────────────────────────────────────────────
ax5 = fig.add_subplot(gs[3, :])
style_ax(ax5, "Composite Overheating Index — All Tickers Ranked (Higher = More Overheated)")
bar_colors = [plt.cm.RdYlGn_r(v) for v in latest_df["composite"][::-1]]
bars = ax5.barh(latest_df.index[::-1], latest_df["composite"][::-1],
                color=bar_colors, edgecolor="#1a1d27", height=0.6)
ax5.axvline(0.75, color="#ef5350", ls="--", lw=1.3, label="Overheating threshold (0.75)")
ax5.axvline(0.25, color="#66bb6a", ls="--", lw=1.3, label="Oversold threshold (0.25)")
ax5.set_xlim(0, 1.08); ax5.set_xlabel("Composite Score")
for bar, v in zip(bars, latest_df["composite"][::-1]):
    ax5.text(v + 0.012, bar.get_y() + bar.get_height() / 2,
             f"{v:.2f}", va="center", fontsize=10, color=TITLE_COL, fontweight="bold")
ax5.legend(fontsize=9, facecolor=AXIS_BG, labelcolor=LABEL_COL)
ax5.tick_params(axis="y", labelcolor=TITLE_COL)

# ── footer ───────────────────────────────────────────────────────────────────────
fig.text(
    0.5, 0.005,
    f"Data: Realistic synthetic prices (GBM, piecewise drift)  |  "
    f"Generated: {datetime.today().strftime('%Y-%m-%d')}  |  "
    "Signals: RSI-14 · Price/SMA-200 stretch · 63-day rolling z-score  (equal-weight composite)",
    ha="center", fontsize=8, color="#666688",
)

out = "/home/user/mycode/semiconductor_overheating.png"
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print(f"Chart saved → {out}")

# ── Console summary ──────────────────────────────────────────────────────────────
print(f"\n── Overheating Snapshot  {END} ──────────────────────────────────────────")
print(f"{'Ticker':<6} {'Name':<22} {'Price':>8} {'RSI':>7} {'Stretch%':>9} {'Score':>7}  {'Signal'}")
print("─" * 72)
for tk, row in latest_df.iterrows():
    if row["composite"] >= 0.75:
        sig = "OVERHEATED 🔥"
    elif row["composite"] <= 0.25:
        sig = "OVERSOLD   ❄️"
    else:
        sig = "Neutral"
    print(f"{tk:<6} {SEMIS[tk]:<22} {row['price']:>8.1f} {row['rsi']:>7.1f} "
          f"{row['stretch']:>8.1f}% {row['composite']:>7.2f}  {sig}")
print("─" * 72)
print("Score: 0.0 = very cold · 0.5 = neutral · 1.0 = severely overheated")
