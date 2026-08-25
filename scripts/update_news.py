import json
from datetime import datetime

import feedparser

FEEDS = [

    {
        "source": "Reuters Business",
        "url": "https://feeds.reuters.com/reuters/businessNews"
    },

    {
        "source": "Reuters World",
        "url": "https://feeds.reuters.com/Reuters/worldNews"
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
            "Source:",
            feed["source"]
        )

        print(
            "Entries:",
            len(rss.entries)
        )

        for entry in rss.entries[:10]:

            title = (
                entry.title.strip()
            )

            if title in seen_titles:
                continue

            seen_titles.add(
                title
            )

            items.append({

                "title": title,

                "source":
                    feed["source"],

                "url":
                    entry.link

            })

    except Exception as e:

        print(
            f"Error with {feed['source']}: {e}"
        )

output = {

    "lastUpdate":
        datetime.utcnow().strftime(
            "%Y-%m-%d %H:%M UTC"
        ),

    "news":
        items[:20]

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
