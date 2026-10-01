"""Turn the raw daily pulls into one table of derived fields.

We publish only: event id, date, country code, AIM label (incident or hazard),
number of articles, languages, harm types, autonomy level, whether the
severity field is filled, a rough "mentions agents" flag, and the AI Incident
Database ids that AIM links to the event. No titles,
summaries or article text go into the table.

The agent flag is a keyword rule on title and summary. It is rough on
purpose (it can catch "travel agent" for example), we use it only to watch the
trend, and it will be checked by hand later.

Usage: python src/build_table.py
"""

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "events.csv"

AGENT_RE = re.compile(r"\b(ai agents?|agentic|autonomous agents?|agents?)\b", re.I)

FIELDS = [
    "id", "date", "country_code", "aim_label", "n_articles", "languages",
    "n_languages", "harm_types", "autonomy_level", "severity_filled",
    "agent_mention", "aiid_ids",
]


def label(props: dict) -> str:
    levels = props.get("harm_levels") or []
    if "AI incident" in levels:
        return "incident"
    if "AI hazard" in levels:
        return "hazard"
    return "other"


def rows():
    seen = set()
    for f in sorted(RAW.glob("*.json")):
        for ev in json.loads(f.read_text())["incidents"]:
            if ev["id"] in seen:
                continue
            seen.add(ev["id"])
            props = ev.get("properties") or {}
            langs = sorted((ev.get("language_counts") or {}).keys())
            text = f"{ev.get('title') or ''} {ev.get('summary') or ''}"
            yield {
                "id": ev["id"],
                "date": ev["date"],
                "country_code": (ev.get("location") or {}).get("country_code") or "",
                "aim_label": label(props),
                "n_articles": ev.get("n_articles") or 0,
                "languages": ";".join(langs),
                "n_languages": len(langs),
                "harm_types": ";".join(props.get("harm_types") or []),
                "autonomy_level": props.get("autonomy_level") or "",
                "severity_filled": int(bool(props.get("most_severe_harm"))),
                "agent_mention": int(bool(AGENT_RE.search(text))),
                # link to the AI Incident Database: groups AIM events that
                # are news fragments of the same real incident
                "aiid_ids": ";".join(str(i) for i in (ev.get("aiid_ids") or [])),
            }


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    data = list(rows())
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(data)
    print(f"{len(data)} events written to {OUT}")


if __name__ == "__main__":
    main()
