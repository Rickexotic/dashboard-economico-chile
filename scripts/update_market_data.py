import json
from datetime import datetime

import yfinance as yf

TICKERS = {
    "SQM-B": "SQM-B.SN",
    "COPEC": "COPEC.SN",
    "CMPC": "CMPC.SN",
    "BCI": "BCI.SN",
    "BSANTANDER": "BSANTANDER.SN",
    "FALABELLA": "FALABELLA.SN",
    "CENCOSUD": "CENCOSUD.SN",
    "RIPLEY": "RIPLEY.SN",
    "ENELAM": "ENELAM.SN",
    "ENELCHILE": "ENELCHILE.SN",
    "ANDINA-B": "ANDINA-B.SN",
    "IAM": "IAM.SN",
    "AGUAS-A": "AGUAS-A.SN",
    "CAP": "CAP.SN",
    "SONDA": "SONDA.SN",
    "PARAUCO": "PARAUCO.SN",
    "MALLPLAZA": "MALLPLAZA.SN",
    "VAPORES": "VAPORES.SN",
    "CCU": "CCU.SN",
    "CONCHATORO": "CONCHATORO.SN"
}

stocks = []

for ticker_name, yahoo_ticker in TICKERS.items():

    try:

        ticker = yf.Ticker(yahoo_ticker)

        hist = ticker.history(period="5d")

        if len(hist) < 2:
            continue

        last = float(hist["Close"].iloc[-1])
        prev = float(hist["Close"].iloc[-2])

        pct = ((last - prev) / prev) * 100
        clp = last - prev

        stocks.append({
            "ticker": ticker_name,
            "precio": round(last, 2),
            "cambioPct": round(pct, 2),
            "cambioClp": round(clp, 2),
            "up": clp >= 0
        })

    except Exception as e:

        print(f"Error processing {ticker_name}: {e}")

output = {
    "meta": {
        "lastUpdate": datetime.utcnow().strftime(
            "%Y-%m-%d %H:%M UTC"
        )
    },
    "stocks": stocks
}

with open(
    "data/stocks.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        output,
        f,
        indent=2,
        ensure_ascii=False
    )

print(
    f"stocks.json updated with {len(stocks)} stocks"
)
