import json
from datetime import datetime
import yfinance as yf

TICKERS = {
    "SQM-B": {"yf": "SQM-B.SN", "empresa": "Sociedad Química y Minera", "sector": "Minería"},
    "COPEC": {"yf": "COPEC.SN", "empresa": "Empresas Copec", "sector": "Energía"},
    "CMPC": {"yf": "CMPC.SN", "empresa": "CMPC", "sector": "Forestal"},
    "BCI": {"yf": "BCI.SN", "empresa": "Banco BCI", "sector": "Bancos"},
    "BSANTANDER": {"yf": "BSANTANDER.SN", "empresa": "Banco Santander Chile", "sector": "Bancos"},
    "FALABELLA": {"yf": "FALABELLA.SN", "empresa": "Falabella", "sector": "Retail"},
    "CENCOSUD": {"yf": "CENCOSUD.SN", "empresa": "Cencosud", "sector": "Retail"},
    "RIPLEY": {"yf": "RIPLEY.SN", "empresa": "Ripley", "sector": "Retail"},
    "ENELAM": {"yf": "ENELAM.SN", "empresa": "Enel Américas", "sector": "Utilities"},
    "ENELCHILE": {"yf": "ENELCHILE.SN", "empresa": "Enel Chile", "sector": "Utilities"},
    "ANDINA-B": {"yf": "ANDINA-B.SN", "empresa": "Embotelladora Andina", "sector": "Consumo"},
    "IAM": {"yf": "IAM.SN", "empresa": "Inversiones Aguas Metropolitanas", "sector": "Utilities"},
    "AGUAS-A": {"yf": "AGUAS-A.SN", "empresa": "Aguas Andinas", "sector": "Utilities"},
    "CAP": {"yf": "CAP.SN", "empresa": "CAP", "sector": "Minería"},
    "SONDA": {"yf": "SONDA.SN", "empresa": "SONDA", "sector": "Tecnología"},
    "PARAUCO": {"yf": "PARAUCO.SN", "empresa": "Parque Arauco", "sector": "Inmobiliario"},
    "MALLPLAZA": {"yf": "MALLPLAZA.SN", "empresa": "Mallplaza", "sector": "Inmobiliario"},
    "VAPORES": {"yf": "VAPORES.SN", "empresa": "Compañía Sud Americana de Vapores", "sector": "Transporte"},
    "CCU": {"yf": "CCU.SN", "empresa": "Compañía Cervecerías Unidas", "sector": "Consumo"},
    "CONCHATORO": {"yf": "CONCHATORO.SN", "empresa": "Viña Concha y Toro", "sector": "Consumo"}
}

stocks = []
history_output = {}

for ticker_name, info in TICKERS.items():

    try:

        ticker = yf.Ticker(info["yf"])

        hist_5d = ticker.history(period="5d")
        hist_1m = ticker.history(period="1mo")
        hist_6m = ticker.history(period="6mo")
        hist_ytd = ticker.history(period="ytd")
        hist_1y = ticker.history(period="1y")
        hist_5y = ticker.history(period="5y")

        print(ticker_name, len(hist_5d))

        if len(hist_5d) < 2:
            print(f"Skipping {ticker_name}")
            continue
import math
        last = float(hist_5d["Close"].iloc[-1])
        prev = float(hist_5d["Close"].iloc[-2])

if (
    math.isnan(last)
    or math.isnan(prev)
):
    print(f"Skipping {ticker_name}: NaN data")
    continue

        if prev == 0:
    continue

        pct = ((last - prev) / prev) * 100
        clp = last - prev

        stocks.append({
            "ticker": ticker_name,
            "empresa": info["empresa"],
            "sector": info["sector"],
            "precio": round(last, 2),
            "cambioPct": round(pct, 2),
            "cambioClp": round(clp, 2),
            "up": clp >= 0
        })

        history_output[ticker_name] = {
            "5D": [round(float(x), 2) for x in hist_5d["Close"].dropna().tolist()],
            "1M": [round(float(x), 2) for x in hist_1m["Close"].dropna().tolist()],
            "6M": [round(float(x), 2) for x in hist_6m["Close"].dropna().tolist()],
            "YTD": [round(float(x), 2) for x in hist_ytd["Close"].dropna().tolist()],
            "1A": [round(float(x), 2) for x in hist_1y["Close"].dropna().tolist()],
            "5A": [round(float(x), 2) for x in hist_5y["Close"].dropna().tolist()]
        }

    except Exception as e:

        print(f"Error processing {ticker_name}: {e}")

timestamp = datetime.utcnow().strftime(
    "%Y-%m-%d %H:%M UTC"
)

stocks_output = {
    "meta": {
        "lastUpdate": timestamp
    },
    "stocks": stocks
}

history_output["meta"] = {
    "lastUpdate": timestamp
}

with open(
    "data/stocks.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        stocks_output,
        f,
        indent=2,
        ensure_ascii=False
    )

with open(
    "data/stock-history.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        history_output,
        f,
        indent=2,
        ensure_ascii=False
    )

print(
    f"stocks.json updated with {len(stocks)} stocks"
)

print(
    f"stock-history.json updated with {len(history_output)-1} stocks"
)
