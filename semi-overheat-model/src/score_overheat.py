"""
Bayesian log-odds model for semiconductor sector overheat probability.

Prior: 10-year SOX cycle context using Capex/D&A ratio and DIO level.
Evidence updates (log-odds):
  1. P/E deviation from historical norm
  2. P/S deviation from historical norm
  3. Price momentum (52-week return z-score)
  4. DIO Q/Q change (inventory build-up signal)
  5. Capex surplus (Capex growth > Revenue growth)
  6. Market sentiment (VIX-based)

Output: posterior overheat probability per week.
"""

import argparse
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path


# ---------------------------------------------------------------------------
# Prior calibration
# ---------------------------------------------------------------------------
# Historical base rate: SOX has experienced severe drawdown (>25%) roughly
# 3-4 times over the past 10 years → ~30-35% of weeks are in "overheat" zone.
PRIOR_LOG_ODDS_BASE = np.log(0.30 / 0.70)   # ≈ -0.847


def compute_prior(row):
    """
    Adjust prior based on long-cycle signals: DIO level and price momentum.
    High DIO + strong momentum → higher prior.
    """
    log_odds = PRIOR_LOG_ODDS_BASE

    # DIO level: > 80 days historically signals inventory excess
    dio_excess = (row["dio"] - 65.0) / 30.0   # normalise; 65=hist median
    log_odds += 0.4 * np.clip(dio_excess, -2, 2)

    # Long-run momentum (already z-scored)
    log_odds += 0.3 * np.clip(row["price_momentum_z"], -3, 3)

    return log_odds


# ---------------------------------------------------------------------------
# Evidence weights (log-likelihood ratios)
# These are calibrated heuristically against historical SOX drawdown episodes.
# ---------------------------------------------------------------------------
EVIDENCE_WEIGHTS = {
    "pe_dev":        1.2,   # P/E above hist norm: strong overheat signal
    "ps_dev":        0.9,   # P/S above hist norm
    "price_momentum_z": 0.5,  # Momentum confirms trend
    "dio_qoq":       0.8,   # Inventory build-up Q/Q
    "capex_surplus": 1.0,   # Capex growing faster than revenue → bubble
    "sentiment_z":   0.6,   # High sentiment (low fear) → complacency
}


def compute_log_likelihood(row):
    """Sum of weighted evidence signals."""
    total = 0.0
    contributions = {}

    # P/E deviation: clip to [-2, 3] range
    pe_signal = np.clip(row["pe_dev"], -1.0, 2.0)
    contributions["pe_dev"] = EVIDENCE_WEIGHTS["pe_dev"] * pe_signal
    total += contributions["pe_dev"]

    # P/S deviation
    ps_signal = np.clip(row["ps_dev"], -1.0, 2.0)
    contributions["ps_dev"] = EVIDENCE_WEIGHTS["ps_dev"] * ps_signal
    total += contributions["ps_dev"]

    # Price momentum z-score
    mom = np.clip(row["price_momentum_z"], -3, 3)
    contributions["price_momentum_z"] = EVIDENCE_WEIGHTS["price_momentum_z"] * mom
    total += contributions["price_momentum_z"]

    # DIO Q/Q change: positive = inventory building (bearish)
    dio_qoq = np.clip(row["dio_qoq"], -1.0, 1.0)
    contributions["dio_qoq"] = EVIDENCE_WEIGHTS["dio_qoq"] * dio_qoq
    total += contributions["dio_qoq"]

    # Capex surplus: positive = overinvestment
    cs = np.clip(row["capex_surplus"], -0.3, 0.5)
    contributions["capex_surplus"] = EVIDENCE_WEIGHTS["capex_surplus"] * cs
    total += contributions["capex_surplus"]

    # Sentiment
    sent = np.clip(row["sentiment_z"], -3, 3)
    contributions["sentiment_z"] = EVIDENCE_WEIGHTS["sentiment_z"] * sent
    total += contributions["sentiment_z"]

    return total, contributions


def log_odds_to_prob(lo):
    return 1.0 / (1.0 + np.exp(-lo))


def score_all(df):
    results = []
    for date, row in df.iterrows():
        prior_lo = compute_prior(row)
        evidence_lo, contribs = compute_log_likelihood(row)
        posterior_lo = prior_lo + evidence_lo
        prior_prob = log_odds_to_prob(prior_lo)
        posterior_prob = log_odds_to_prob(posterior_lo)
        record = {
            "date": date,
            "sox_close": row["sox_close"],
            "prior_prob": round(prior_prob, 4),
            "posterior_prob": round(posterior_prob, 4),
            "prior_log_odds": round(prior_lo, 4),
            "evidence_log_odds": round(evidence_lo, 4),
            "posterior_log_odds": round(posterior_lo, 4),
        }
        for k, v in contribs.items():
            record[f"contrib_{k}"] = round(v, 4)
        results.append(record)
    return pd.DataFrame(results).set_index("date")


def plot_results(scores, out_path):
    fig, ax = plt.subplots(figsize=(14, 5))

    ax.plot(scores.index, scores["posterior_prob"], color="#c0392b", lw=1.5,
            label="Posterior", alpha=0.9)
    ax.plot(scores.index, scores["prior_prob"], color="#5dade2", lw=1.2,
            linestyle="--", label="Prior", alpha=0.8)

    ax.axhline(0.65, color="#e74c3c", linestyle=":", lw=1.0, alpha=0.7)
    ax.axhline(0.50, color="#f39c12", linestyle=":", lw=1.0, alpha=0.7)

    ax.fill_between(scores.index, scores["posterior_prob"], 0.65,
                    where=scores["posterior_prob"] >= 0.65,
                    color="#c0392b", alpha=0.15)

    ax.set_ylim(0, 1)
    ax.set_ylabel("Probability")
    ax.set_title("Semiconductor Sector Overheat Probability", fontsize=13)
    ax.legend(loc="upper left", fontsize=9)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Chart saved to {out_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",  default="data/raw/weekly_observations.csv")
    parser.add_argument("--output", default="reports/latest_score.csv")
    args = parser.parse_args()

    df = pd.read_csv(args.input, index_col="date", parse_dates=True)
    print(f"Loaded {len(df)} weekly rows from {args.input}")

    scores = score_all(df)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    scores.to_csv(args.output)
    print(f"Scores saved to {args.output}")

    latest = scores.iloc[-1]
    print(f"\n=== Latest week: {scores.index[-1].date()} ===")
    print(f"  Prior prob     : {latest['prior_prob']:.1%}")
    print(f"  Posterior prob : {latest['posterior_prob']:.1%}")
    print(f"  Evidence LLR   : {latest['evidence_log_odds']:+.3f}")
    contrib_cols = [c for c in scores.columns if c.startswith("contrib_")]
    print("\n  Evidence contributions (log-odds):")
    for c in contrib_cols:
        print(f"    {c[8:]:25s}: {latest[c]:+.3f}")

    chart_path = str(Path(args.output).parent / "latest_score.png")
    plot_results(scores, chart_path)


if __name__ == "__main__":
    main()
