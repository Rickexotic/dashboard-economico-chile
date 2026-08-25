import json
from datetime import datetime

import feedparser

FEEDS = [
    {
        "source": "Diario Financiero",
        "url": "https://www.df.cl/noticias/site/list/port/rss____1.xml"
    }
]

items = []
seen_titles = set()

for feed in FEEDS:

    try:

        rss = feedparser.parse(feed["url"])

print("================================")
print("Source:", feed["source"])
print("URL:", feed["url"])
print("Feed title:", rss.feed.get("title", "N/A"))
print("Entries:", len(rss.entries))
print("Bozo:", rss.bozo)

if rss.bozo:
    print("Error:", rss.bozo_exception)

for entry in rss.entries[:3]:
    print("TITLE:", entry.title)
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
