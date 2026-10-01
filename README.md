# How severe? AI incidents on the OECD severity ladder

**Status: work in progress (started October 2026).**

This project tests if news-reported AI incidents can be placed, in a reliable
way, on the five-level severity ladder that the OECD proposes: hazard, serious
hazard, incident, serious incident, disaster.

It uses public data from the OECD AI Incidents and Hazards Monitor (AIM).
**This project is not affiliated with, or endorsed by, the OECD.**

## Why this question

Two OECD texts point to the same gap.

- The 2024 definitions paper says: "Assessing the 'seriousness' of an AI
  incident ... is context-dependent and is also left for further discussion"
  (OECD, *Defining AI incidents and related terms*, 2024, p. 15).
- The 2025 reporting framework makes severity a mandatory field, and says it
  is "essential" that incidents from the media "are tagged using the criteria
  defined within the framework" (OECD, *Towards a common reporting framework
  for AI incidents*, 2025, p. 19).

In the public AIM data, the field `most_severe_harm` is empty for all 5,309
events from January to September 2026 (see `results/descriptives.md`). So we
ask: if we want to fill it, how consistently can it be done from what AIM holds?

AIM also splits one real incident into several news events. In the same
period, 47 AI Incident Database incidents are spread over 159 AIM events (one
incident alone has 26). The OECD defines an incident as an "event,
circumstance or series of events" (2024, p. 11). So we also ask whether the
rung changes with which fragment is coded.

## Related work

CSET (AI Incident Database annotations) and the MIT AI Incident Tracker have
coded severity before. Neither publishes agreement figures that I could find.
This project uses the OECD ladder, AIM data, and reports agreement openly.

## Plan

1. Codebook: turn the OECD definitions into written decision rules (`codebook/`).
2. Sample about 300 events, stratified by month, incident or hazard, harm
   type, agent-related events, and events reported mainly in Spanish or French.
3. A classifier agent (an LLM with the codebook) gives each event a rung and a reason.
4. A checker agent codes the same events blind, without seeing the first answer.
   Disagreements go to a third pass that must cite the codebook rule.
5. I hand-code about 150 events before seeing any model output, and recode
   30 of them two weeks later to measure my own consistency.
6. Agreement statistics (weighted kappa, Krippendorff's alpha, bootstrap
   intervals), and where the disagreements are: by harm type, agent-related
   or not, and language.
7. A short note on what can and cannot be said about severity from news data.

Low agreement is also a valid result. The point is to measure it, not to say
that AIM is right or wrong.

## Done so far

- [x] `src/pull.py`: pulls AIM events day by day (one call per day, below the 100 cap) and caches them.
- [x] `src/build_table.py`: keeps only derived fields in `data/events.csv`.
- [x] `src/descriptives.py`: first numbers in `results/descriptives.md`.
- [x] `codebook/codebook-v0.md`: first draft of the rules.
- [x] AI Incident Database links (`aiid_ids`) in the table, to group fragments of the same incident.
- [ ] Sample and hand-coding.
- [ ] Classifier and checker agents.
- [ ] Agreement statistics and the note.

## First numbers (January to September 2026)

- 5,309 events, about 19 per day. 59% to 74% per month are labelled as incidents, the rest as hazards.
- Severity field filled: 0 of 5,309.
- Autonomy level is filled for 70% of events; 36% of all events are coded "high-action autonomy".
- Events that mention agents (rough keyword rule, not checked by hand yet) went from 2.7% in January to 12.1% in September.
- Between 22% and 33% of events per month have articles in more than one language. English is in 2,907 events, Spanish in 853, French in 493.

## Reproduce

Python 3.10 or newer, no extra packages.

```
python src/pull.py 2026-01-01 2026-09-30
python src/build_table.py
python src/descriptives.py
```

## Data and licence

- The API is public and undocumented, so the code caches every pull. Raw pulls
  stay local (`data/raw/` is not in git) because they contain AIM titles and
  summaries.
- This repository publishes only AIM event IDs, dates, derived fields, my own
  labels and totals. No article text, images or copies of AIM summaries. To see
  an event, open it on the AIM website.
- Data source: OECD AI Incidents and Hazards Monitor, https://oecd.ai/en/incidents,
  used under the OECD terms and conditions. OECD papers quoted here are CC BY 4.0.
- Code: MIT licence. My derived labels: CC BY 4.0.

## Author

Felipe Alvarez, M2 student in AI (CNAM Paris).
