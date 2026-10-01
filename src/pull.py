"""Pull AI incident events from the public AIM API, one day per call.

AIM is the OECD AI Incidents and Hazards Monitor (https://oecd.ai/en/incidents).
The API is public and needs no key, but it is not documented, so we cache every
day on disk the first time. One call returns at most 100 events, and no day so
far has more than 100, so one call per day is enough. We check this anyway.

Raw files go to data/raw/ and are NOT committed, because they hold AIM titles
and summaries. Only derived fields are published (see build_table.py).

Usage: python src/pull.py 2026-01-01 2026-09-30
"""

import datetime as dt
import json
import sys
import time
import urllib.request
from pathlib import Path

API = "https://incidents-server.oecdai.org/api/v1/incidents/fetch-incidents"
RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
MAX_PER_CALL = 100


def fetch_day(day: str) -> dict:
    body = {
        "search_terms": [],
        "countries": [],
        "and_condition": False,
        "from_date": day,
        "to_date": day,
        "properties_config": {},
        "num_results": MAX_PER_CALL,
        "format": "JSON",
    }
    req = urllib.request.Request(
        API,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    # we keep only what we need, the time series are recomputed later
    return {"total_results": data["total_results"], "incidents": data["incidents"]}


def main(start: str, end: str) -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    d0 = dt.date.fromisoformat(start)
    d1 = dt.date.fromisoformat(end)
    capped = []
    day = d0
    while day <= d1:
        out = RAW / f"{day.isoformat()}.json"
        if not out.exists():
            data = fetch_day(day.isoformat())
            out.write_text(json.dumps(data, ensure_ascii=False))
            time.sleep(0.5)  # be gentle with a public server
        else:
            data = json.loads(out.read_text())
        if data["total_results"] > len(data["incidents"]):
            capped.append(day.isoformat())
        day += dt.timedelta(days=1)
    print(f"pulled {start} to {end} into {RAW}")
    if capped:
        print("WARNING: these days hit the 100 cap, some events are missing:", capped)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
