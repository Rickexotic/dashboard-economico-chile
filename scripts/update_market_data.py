import json
from datetime import datetime

output = {
    "meta": {
        "lastUpdate": datetime.now().strftime(
            "%Y-%m-%d %H:%M UTC"
        )
    }
}

with open(
    "data/stock-history.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        output,
        f,
        indent=2,
        ensure_ascii=False
    )

print("stock-history.json updated")
