import json
from datetime import datetime
import yfinance as yf

TICKERS = [
    "SQM-B.SN",
    "COPEC.SN",
    "CMPC.SN",
    "BCI.SN",
    "BSANTANDER.SN",
    "FALABELLA.SN"
]

results = {}

for ticker in TICKERS:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d")

        results[ticker] = {
            "rows": len(hist)
        }

    except Exception as e:
        results[ticker] = {
            "error": str(e)
        }

with open(
    "data/update-status.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        {
            "lastUpdate":
                datetime.utcnow().strftime(
                    "%Y-%m-%d %H:%M UTC"
                ),
            "tickers": results
        },
        f,
        indent=2,
        ensure_ascii=False
    )

print("Update completed")
