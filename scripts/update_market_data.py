import json
from datetime import datetime

import yfinance as yf

TICKERS = {

    "SQM-B": {
        "yf": "SQM-B.SN",
        "empresa": "Sociedad Química y Minera",
        "sector": "Minería"
    },

    "COPEC": {
        "yf": "COPEC.SN",
        "empresa": "Empresas Copec",
        "sector": "Energía"
    },

    "CMPC": {
        "yf": "CMPC.SN",
        "empresa": "CMPC",
        "sector": "Forestal"
    },

    "BCI": {
        "yf": "BCI.SN",
        "empresa": "Banco BCI",
        "sector": "Bancos"
    },

    "BSANTANDER": {
        "yf": "BSANTANDER.SN",
        "empresa": "Banco Santander Chile",
        "sector": "Bancos"
    },

    "FALABELLA": {
        "yf": "FALABELLA.SN",
        "empresa": "Falabella",
        "sector": "Retail"
    },

    "CENCOSUD": {
        "yf": "CENCOSUD.SN",
        "empresa": "Cencosud",
        "sector": "Retail"
    },

    "RIPLEY": {
        "yf": "RIPLEY.SN",
        "empresa": "Ripley",
        "sector": "Retail"
    },

    "ENELAM": {
        "yf": "ENELAM.SN",
        "empresa": "Enel Américas",
        "sector": "Utilities"
    },

    "ENELCHILE": {
        "yf": "ENELCHILE.SN",
        "empresa": "Enel Chile",
        "sector": "Utilities"
    },

    "ANDINA-B": {
        "yf": "ANDINA-B.SN",
        "empresa": "Embotelladora Andina",
        "sector": "Consumo"
    },

    "IAM": {
        "yf": "IAM.SN",
        "empresa": "Inversiones Aguas Metropolitanas",
        "sector": "Utilities"
    },

    "AGUAS-A": {
        "yf": "AGUAS-A.SN",
        "empresa": "Aguas Andinas",
        "sector": "Utilities"
    },

    "CAP": {
        "yf": "CAP.SN",
        "empresa": "CAP",
        "sector": "Minería"
    },

    "SONDA": {
        "yf": "SONDA.SN",
        "empresa": "SONDA",
        "sector": "Tecnología"
    },

    "PARAUCO": {
        "yf": "PARAUCO.SN",
        "empresa": "Parque Arauco",
        "sector": "Inmobiliario"
    },

    "MALLPLAZA": {
        "yf": "MALLPLAZA.SN",
        "empresa": "Mallplaza",
        "sector": "Inmobiliario"
    },

    "VAPORES": {
        "yf": "VAPORES.SN",
        "empresa": "Compañía Sud Americana de Vapores",
        "sector": "Transporte"
    },

    "CCU": {
        "yf": "CCU.SN",
        "empresa": "Compañía Cervecerías Unidas",
        "sector": "Consumo"
    },

    "CONCHATORO": {
        "yf": "CONCHATORO.SN",
        "empresa": "Viña Concha y Toro",
        "sector": "Consumo"
    }

}
stocks = []

for ticker_name, yahoo_ticker in TICKERS.items():

    try:

        ticker = yf.Ticker(yahoo_ticker)

        hist = ticker.history(period="5d")
        print(ticker_name, len(hist))

       if len(hist) < 2:
           print(f"Skipping {ticker_name}")
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
