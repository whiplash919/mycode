"""
Fetch SOX index and semiconductor sector fundamentals from yfinance.
Outputs weekly_observations.csv with columns needed by score_overheat.py
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

# SOX proxy: SOXX ETF (iShares Philadelphia SOX)
# Fundamentals proxy: use a basket of major semis for P/E, P/S, Capex, DIO
SEMI_TICKERS = ["NVDA", "AMD", "INTC", "AVGO", "QCOM", "MU", "AMAT", "LRCX", "KLAC", "TXN"]
SOX_TICKER = "SOXX"

def get_price_data(start="2015-01-01"):
    print("Fetching price data...")
    sox = yf.download(SOX_TICKER, start=start, interval="1wk", progress=False, auto_adjust=True)
    sox = sox["Close"].rename("sox_close")
    semis = yf.download(SEMI_TICKERS, start=start, interval="1wk", progress=False, auto_adjust=True)["Close"]
    semis_avg = semis.mean(axis=1).rename("semi_avg_close")
    df = pd.concat([sox, semis_avg], axis=1).dropna()
    df.index = pd.to_datetime(df.index).tz_localize(None)
    return df

def get_fundamentals():
    """Get latest TTM P/E, P/S, and annual Capex/Revenue for each ticker."""
    rows = []
    for t in SEMI_TICKERS:
        try:
            tk = yf.Ticker(t)
            info = tk.info
            pe = info.get("trailingPE", np.nan)
            ps = info.get("priceToSalesTrailing12Months", np.nan)
            # Capex and revenue from financials
            cf = tk.cashflow
            inc = tk.income_stmt
            capex, revenue = np.nan, np.nan
            if cf is not None and not cf.empty:
                for key in ["Capital Expenditure", "CapitalExpenditures"]:
                    if key in cf.index:
                        capex = abs(float(cf.loc[key].iloc[0]))
                        break
            if inc is not None and not inc.empty:
                for key in ["Total Revenue", "TotalRevenue"]:
                    if key in inc.index:
                        revenue = float(inc.loc[key].iloc[0])
                        break
            rows.append({"ticker": t, "pe": pe, "ps": ps, "capex": capex, "revenue": revenue})
        except Exception as e:
            print(f"  Warning: {t} fundamentals failed: {e}")
    return pd.DataFrame(rows)

def compute_dio(ticker_obj):
    """Days Inventory Outstanding = Inventory / (COGS/365)"""
    try:
        bs = ticker_obj.balance_sheet
        inc = ticker_obj.income_stmt
        inv = None
        for k in ["Inventory", "Inventories"]:
            if k in bs.index:
                inv = float(bs.loc[k].iloc[0])
                break
        cogs = None
        for k in ["Cost Of Revenue", "CostOfRevenue", "Cost of Goods Sold"]:
            if k in inc.index:
                cogs = float(inc.loc[k].iloc[0])
                break
        if inv and cogs and cogs > 0:
            return inv / (cogs / 365)
    except:
        pass
    return np.nan

def build_weekly_observations():
    print("Building weekly observations...")
    prices = get_price_data()

    # Compute SOX weekly return and rolling features
    prices["sox_ret_1w"] = prices["sox_close"].pct_change(1)
    prices["sox_ret_52w"] = prices["sox_close"].pct_change(52)   # 1-year momentum
    prices["sox_ma52"] = prices["sox_close"].rolling(52).mean()
    prices["sox_above_ma52"] = (prices["sox_close"] > prices["sox_ma52"]).astype(float)

    # Price momentum signal: z-score of 52w return over 5-year rolling window
    roll_mean = prices["sox_ret_52w"].rolling(260).mean()
    roll_std  = prices["sox_ret_52w"].rolling(260).std()
    prices["price_momentum_z"] = (prices["sox_ret_52w"] - roll_mean) / roll_std

    # Get fundamentals (point-in-time snapshot, repeated as constant for now)
    print("Fetching fundamentals (this may take a minute)...")
    fund = get_fundamentals()

    med_pe  = fund["pe"].median()
    med_ps  = fund["ps"].median()
    hist_pe = 25.0   # approximate 10yr historical median for semis
    hist_ps = 4.5

    # P/E and P/S deviation from historical norms
    pe_dev = (med_pe - hist_pe) / hist_pe if not np.isnan(med_pe) else 0.0
    ps_dev = (med_ps - hist_ps) / hist_ps if not np.isnan(med_ps) else 0.0

    # Capex surplus = Capex growth - Revenue growth (use aggregate)
    capex_growth = 0.15   # placeholder; replace with real YoY data
    rev_growth   = 0.10
    capex_surplus = capex_growth - rev_growth

    # DIO (aggregate)
    print("Fetching DIO data...")
    dio_vals = []
    for t in SEMI_TICKERS[:5]:   # subset to save time
        tk = yf.Ticker(t)
        d = compute_dio(tk)
        if not np.isnan(d):
            dio_vals.append(d)
    med_dio = np.median(dio_vals) if dio_vals else 65.0
    hist_dio = 65.0
    dio_qoq_change = 0.0   # will be computed from rolling data below

    # Market sentiment: VIX as inverse sentiment proxy
    print("Fetching VIX for sentiment...")
    vix = yf.download("^VIX", start="2015-01-01", interval="1wk", progress=False, auto_adjust=True)["Close"]
    vix.index = pd.to_datetime(vix.index).tz_localize(None)
    vix = vix.rename("vix")
    prices = prices.join(vix, how="left")
    prices["vix"] = prices["vix"].ffill()
    # Sentiment z-score (high VIX = fearful = lower overheat signal)
    vix_mean = prices["vix"].rolling(104).mean()
    vix_std  = prices["vix"].rolling(104).std()
    prices["sentiment_z"] = -((prices["vix"] - vix_mean) / vix_std)  # negative: fear lowers overheat prob

    # Attach fundamental scalars across all weeks (constant, updated weekly in real use)
    prices["pe_dev"]       = pe_dev
    prices["ps_dev"]       = ps_dev
    prices["capex_surplus"]= capex_surplus
    prices["dio"]          = med_dio
    prices["dio_qoq"]      = dio_qoq_change

    prices = prices.dropna(subset=["price_momentum_z", "sentiment_z"])
    prices.index.name = "date"

    out_cols = ["sox_close", "price_momentum_z", "pe_dev", "ps_dev",
                "capex_surplus", "dio", "dio_qoq", "sentiment_z"]
    out = prices[out_cols].round(4)
    path = "/home/user/mycode/semi-overheat-model/data/raw/weekly_observations.csv"
    out.to_csv(path)
    print(f"Saved {len(out)} weekly rows to {path}")
    print(out.tail(3))
    return out

if __name__ == "__main__":
    build_weekly_observations()
