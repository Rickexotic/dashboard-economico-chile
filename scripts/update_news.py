import json
from datetime import datetime

import feedparser

FEEDS = [
    {
        "source": "Emol Economía",
        "url": "https://www.emol.com/rss/economia.xml"
    }
]

items = []

for feed in FEEDS:

    try:

        rss = feedparser.parse(
            feed["url"]
        )

        for entry in rss.entries[:10]:

            items.append({

                "title": entry.title,

                "source":
                    feed["source"],

                "url":
                    entry.link

            })

    except Exception as e:

        print(e)

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

print(
    f"News updated: {len(items)} articles"
)
