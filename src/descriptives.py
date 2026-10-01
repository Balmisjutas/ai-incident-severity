"""First descriptive numbers on the derived table.

Writes results/descriptives.md. Plain Python, no extra packages, so anyone can
re-run it after pull.py and build_table.py.

Usage: python src/descriptives.py
"""

import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TABLE = ROOT / "data" / "events.csv"
OUT = ROOT / "results" / "descriptives.md"


def pct(a: int, b: int) -> str:
    return f"{100 * a / b:.1f}%" if b else "-"


def main() -> None:
    ev = list(csv.DictReader(TABLE.open()))
    n = len(ev)
    dates = sorted(e["date"] for e in ev)
    by_month = defaultdict(list)
    for e in ev:
        by_month[e["date"][:7]].append(e)

    lines = [
        "# Descriptive statistics",
        "",
        f"Events: {n}, from {dates[0]} to {dates[-1]}. Source: AIM public API, "
        "pulled with src/pull.py. Derived fields only.",
        "",
        "## Per month",
        "",
        "| Month | Events | Incident share | Severity field filled | Mentions agents | Multilingual |",
        "|---|---|---|---|---|---|",
    ]
    for m in sorted(by_month):
        es = by_month[m]
        k = len(es)
        lines.append(
            f"| {m} | {k} | {pct(sum(e['aim_label'] == 'incident' for e in es), k)} "
            f"| {pct(sum(e['severity_filled'] == '1' for e in es), k)} "
            f"| {pct(sum(e['agent_mention'] == '1' for e in es), k)} "
            f"| {pct(sum(int(e['n_languages']) > 1 for e in es), k)} |"
        )

    harms = Counter(h for e in ev for h in e["harm_types"].split(";") if h)
    lines += ["", "## Harm types (an event can have several)", "", "| Harm type | Events | Share |", "|---|---|---|"]
    for h, c in harms.most_common():
        lines.append(f"| {h} | {c} | {pct(c, n)} |")

    auto = Counter(e["autonomy_level"] or "(empty)" for e in ev)
    lines += ["", "## Autonomy level", "", "| Level | Events | Share |", "|---|---|---|"]
    for a, c in auto.most_common():
        lines.append(f"| {a} | {c} | {pct(c, n)} |")

    langs = Counter(l for e in ev for l in e["languages"].split(";") if l)
    lines += ["", "## Languages (events with at least one article in it), top 10", "", "| Language | Events |", "|---|---|"]
    for l, c in langs.most_common(10):
        lines.append(f"| {l} | {c} |")

    agents = [e for e in ev if e["agent_mention"] == "1"]
    lines += [
        "",
        "## Notes",
        "",
        f"- The severity field (`most_severe_harm`) is filled for "
        f"{sum(e['severity_filled'] == '1' for e in ev)} of {n} events. "
        "This is the gap the project looks at.",
        f"- {len(agents)} events mention agents (rough keyword rule, not checked by hand yet).",
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
