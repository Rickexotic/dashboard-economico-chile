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

                seen_titles.add(title)

                items.append({

                    "title": title,

                    "source":
                        feed["source"],

                    "category":
                        feed["category"],

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

# Limit articles
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
    f"News updated: {len(items)} articles"
)
