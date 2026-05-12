"""LITE DCF model.

Single-file, stdlib-only discounted cash flow valuation.

  python3 dcf_lite.py                          # run with defaults
  python3 dcf_lite.py --revenue 1000 --wacc 0.09 --terminal-growth 0.025

Outputs:
  - 5-year FCFF projection table
  - Enterprise value, equity value, per-share value
  - Sensitivity grid over WACC and terminal growth

FCFF = EBIT*(1-t) + D&A - capex - ΔNWC.
Equity value = EV - net debt.
Terminal value uses Gordon growth on year-5 FCFF.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass


@dataclass
class Inputs:
    revenue: float = 1_000.0          # base-year revenue ($M)
    growth_y1: float = 0.10           # year-1 revenue growth
    growth_terminal: float = 0.03     # year-5 revenue growth (linear decay from y1)
    ebit_margin: float = 0.20
    tax_rate: float = 0.25
    da_pct: float = 0.05              # D&A as % of revenue
    capex_pct: float = 0.06           # capex as % of revenue
    nwc_pct: float = 0.02             # ΔNWC as % of revenue
    wacc: float = 0.09
    terminal_growth: float = 0.025
    net_debt: float = 100.0           # ($M); subtracted from EV
    shares_out: float = 100.0         # (millions)
    years: int = 5


def _decay(g0: float, gT: float, n: int) -> list[float]:
    if n <= 1:
        return [gT]
    step = (g0 - gT) / (n - 1)
    return [g0 - step * i for i in range(n)]


def project(i: Inputs) -> list[dict]:
    growths = _decay(i.growth_y1, i.growth_terminal, i.years)
    rows, rev = [], i.revenue
    for yr, g in enumerate(growths, start=1):
        rev *= 1 + g
        ebit = rev * i.ebit_margin
        nopat = ebit * (1 - i.tax_rate)
        da = rev * i.da_pct
        capex = rev * i.capex_pct
        d_nwc = rev * i.nwc_pct
        fcff = nopat + da - capex - d_nwc
        rows.append({
            "year": yr, "revenue": rev, "ebit": ebit, "nopat": nopat,
            "da": da, "capex": capex, "d_nwc": d_nwc, "fcff": fcff,
        })
    return rows


def value(i: Inputs, rows: list[dict] | None = None) -> dict:
    rows = rows or project(i)
    if i.wacc <= i.terminal_growth:
        raise ValueError("WACC must exceed terminal growth for Gordon model.")
    pv_fcff = sum(r["fcff"] / (1 + i.wacc) ** r["year"] for r in rows)
    tv = rows[-1]["fcff"] * (1 + i.terminal_growth) / (i.wacc - i.terminal_growth)
    pv_tv = tv / (1 + i.wacc) ** i.years
    ev = pv_fcff + pv_tv
    equity = ev - i.net_debt
    return {
        "pv_fcff": pv_fcff, "terminal_value": tv, "pv_terminal": pv_tv,
        "enterprise_value": ev, "equity_value": equity,
        "per_share": equity / i.shares_out if i.shares_out else float("nan"),
    }


def sensitivity(i: Inputs, wacc_range=(-0.02, 0.02, 5), g_range=(-0.01, 0.01, 5)) -> list[list[float]]:
    def grid(center, lo_off, hi_off, n):
        step = (hi_off - lo_off) / (n - 1)
        return [center + lo_off + step * k for k in range(n)]

    waccs = grid(i.wacc, *wacc_range)
    gs = grid(i.terminal_growth, *g_range)
    out = [["WACC \\ g"] + [f"{g:.2%}" for g in gs]]
    rows = project(i)
    for w in waccs:
        line = [f"{w:.2%}"]
        for g in gs:
            try:
                v = value(Inputs(**{**i.__dict__, "wacc": w, "terminal_growth": g}), rows)
                line.append(f"{v['per_share']:.2f}")
            except ValueError:
                line.append("n/a")
        out.append(line)
    return out


def _fmt_table(headers: list[str], rows: list[list[str]]) -> str:
    widths = [max(len(h), *(len(r[c]) for r in rows)) for c, h in enumerate(headers)]
    line = lambda cells: "  ".join(c.rjust(w) for c, w in zip(cells, widths))
    sep = "  ".join("-" * w for w in widths)
    return "\n".join([line(headers), sep, *(line(r) for r in rows)])


def report(i: Inputs) -> str:
    rows = project(i)
    v = value(i, rows)
    proj_headers = ["Year", "Revenue", "EBIT", "NOPAT", "D&A", "Capex", "ΔNWC", "FCFF"]
    proj_body = [[str(r["year"])] + [f"{r[k]:,.1f}" for k in
                  ("revenue", "ebit", "nopat", "da", "capex", "d_nwc", "fcff")] for r in rows]
    sens = sensitivity(i)
    sens_str = _fmt_table(sens[0], sens[1:])
    return (
        "=== DCF LITE ===\n\n"
        f"Assumptions: WACC={i.wacc:.2%}, g∞={i.terminal_growth:.2%}, "
        f"tax={i.tax_rate:.2%}, EBIT margin={i.ebit_margin:.2%}\n\n"
        "Projection ($M):\n"
        + _fmt_table(proj_headers, proj_body)
        + "\n\nValuation ($M):\n"
        f"  PV of explicit FCFF .... {v['pv_fcff']:>12,.1f}\n"
        f"  Terminal value (y{i.years}) ... {v['terminal_value']:>12,.1f}\n"
        f"  PV of terminal value ... {v['pv_terminal']:>12,.1f}\n"
        f"  Enterprise value ....... {v['enterprise_value']:>12,.1f}\n"
        f"  − Net debt ............. {i.net_debt:>12,.1f}\n"
        f"  Equity value ........... {v['equity_value']:>12,.1f}\n"
        f"  Per share .............. ${v['per_share']:>11,.2f}\n\n"
        f"Sensitivity (per-share value, WACC × terminal g):\n{sens_str}\n"
    )


def _cli() -> Inputs:
    p = argparse.ArgumentParser(description="LITE DCF model.")
    defaults = Inputs()
    for f, val in defaults.__dict__.items():
        p.add_argument(f"--{f.replace('_', '-')}", type=type(val), default=val)
    return Inputs(**vars(p.parse_args()))


if __name__ == "__main__":
    print(report(_cli()))
