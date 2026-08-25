import json
from datetime import datetime

import feedparser

FEEDS = [

    {
        "source": "Diario Financiero",
        "url": "https://www.df.cl/noticias/site/list/port/rss____1.xml"
    },

    {
        "source": "The Clinic",
        "url": "https://www.theclinic.cl/feed/"
    },

    {
        "source": "Cambio21",
        "url": "https://cambio21.cl/rss"
    },

    {
        "source": "La Nación",
        "url": "https://lanacion.cl/feed/"
    },

    {
        "source": "El Mostrador",
        "url": "https://www.elmostrador.cl/feed/"
    },

    {
        "source": "La Discusión",
        "url": "https://ladiscusion.cl/feed/"
    }

]

items = []
seen_titles = set()

print("")
print("===== RSS VALIDATION =====")
print("")

for feed in FEEDS:

    try:

        rss = feedparser.parse(
            feed["url"]
        )

        print("--------------------------------")
        print("Source:", feed["source"])
        print("URL:", feed["url"])
        print(
            "Feed title:",
            rss.feed.get("title", "N/A")
        )
        print(
            "Entries:",
            len(rss.entries)
        )
        print(
            "Bozo:",
            rss.bozo
        )

        if rss.bozo:
            print(
                "Error:",
                rss.bozo_exception
            )

        if len(rss.entries) > 0:

            print("First article:")

            try:
                print(
                    rss.entries[0].title
                )
            except Exception:
                pass

        for entry in rss.entries[:5]:

            try:

                title = entry.title.strip()

                if title in seen_titles:
                    continue

                seen_titles.add(title)

                items.append({

                    "title": title,

                    "source":
                        feed["source"],

                    "url":
                        entry.link

                })

            except Exception:
                pass

    except Exception as e:

        print(
            f"ERROR: {feed['source']}"
        )

        print(str(e))

output = {

    "lastUpdate":
        datetime.utcnow().strftime(
            "%Y-%m-%d %H:%M UTC"
        ),

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

print("")
print("===== SUMMARY =====")
print(
    f"News collected: {len(items)}"
)
