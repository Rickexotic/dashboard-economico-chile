import json
from datetime import datetime

with open(
    "data/update-status.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        {
            "lastUpdate": datetime.utcnow().strftime(
                "%Y-%m-%d %H:%M UTC"
            )
        },
        f,
        indent=2
    )

print("update-status.json updated")
