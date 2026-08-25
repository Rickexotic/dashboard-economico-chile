import json
from datetime import datetime

import feedparser

FEEDS = [

    {
        "source": "The Clinic",
        "category": "general",
        "url": "https://www.theclinic.cl/feed/"
    },

    {
        "source": "Cambio21",
        "category": "politica",
        "url": "https://cambio21.cl/rss"
    },

    {
        "source": "La Nación",
        "category": "general",
        "url": "https://lanacion.cl/feed/"
    },

    {
        "source": "La Discusión",
        "category": "regional",
        "url": "https://ladiscusion.cl/feed/"
    }

]

ECONOMIA_KEYWORDS = [
    "economía",
    "economico",
    "económico",
    "inflación",
    "inflacion",
    "ipc",
    "imacec",
    "banco central",
    "tpm",
    "empleo",
    "desempleo",
    "pib",
    "uf",
    "crecimiento",
    "recesión",
    "recesion",
    "actividad económica",
    "actividad economica",
    "hacienda",
    "presupuesto"
]

MERCADOS_KEYWORDS = [
    "ipsa",
    "acciones",
    "bolsa",
    "mercado",
    "mercados",
    "wall street",
    "dólar",
    "dolar",
    "tipo de cambio",
    "peso chileno",
    "inversión",
    "inversion",
    "trading",
    "bonos",
    "commodities",
    "acciones chilenas",
    "sqm",
    "copec",
    "falabella",
    "cmpc",
    "bci"
]

items = []
seen_titles = set()

for feed in FEEDS:

    try:

        rss = feedparser.parse(
            feed["url"]
        )

        print(
            f"{feed['source']}: "
            f"{len(rss.entries)} entries"
        )

        for entry in rss.entries:

            try:

                title = (
                    entry.title.strip()
                )

                if title in seen_titles:
                    continue

                seen_titles.add(
                    title
                )

                text = title.lower()

                category = feed["category"]

                if any(
                    keyword in text
                    for keyword in ECONOMIA_KEYWORDS
                ):
                    category = "economia"

                elif any(
                    keyword in text
                    for keyword in MERCADOS_KEYWORDS
                ):
                    category = "mercados"

                items.append({

                    "title": title,

                    "source":
                        feed["source"],

                    "category":
                        category,

                    "published":
                        entry.get(
                            "published",
                            ""
                        ),

                    "url":
                        entry.get(
                            "link",
                            ""
                        )

                })

            except Exception:
                pass

    except Exception as e:

        print(
            f"Error with "
            f"{feed['source']}: {e}"
        )

# keep latest 30 articles
items = items[:30]

output = {

    "lastUpdate":
        datetime.utcnow().strftime(
            "%Y-%m-%d %H:%M UTC"
        ),

    "totalArticles":
        len(items),

    "news":
        items

}

with open(
    "data/news.json",
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
    f"News updated: "
    f"{len(items)} articles"
)
