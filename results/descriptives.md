# Descriptive statistics

Events: 5309, from 2026-01-01 to 2026-09-30. Source: AIM public API, pulled with src/pull.py. Derived fields only.

## Per month

| Month | Events | Incident share | Severity field filled | Mentions agents | Multilingual |
|---|---|---|---|---|---|
| 2026-01 | 596 | 73.8% | 0.0% | 2.7% | 25.2% |
| 2026-02 | 551 | 66.2% | 0.0% | 5.1% | 28.7% |
| 2026-03 | 594 | 66.3% | 0.0% | 7.1% | 27.6% |
| 2026-04 | 483 | 59.6% | 0.0% | 4.6% | 26.5% |
| 2026-05 | 588 | 63.1% | 0.0% | 2.9% | 23.1% |
| 2026-06 | 640 | 58.9% | 0.0% | 3.6% | 22.0% |
| 2026-07 | 581 | 70.7% | 0.0% | 5.7% | 28.1% |
| 2026-08 | 597 | 68.5% | 0.0% | 6.2% | 28.3% |
| 2026-09 | 679 | 62.4% | 0.0% | 12.1% | 33.0% |

## Harm types (an event can have several)

| Harm type | Events | Share |
|---|---|---|
| Human or fundamental rights | 1850 | 34.8% |
| Economic/Property | 1803 | 34.0% |
| Public interest | 1279 | 24.1% |
| Reputational | 1198 | 22.6% |
| Psychological | 1110 | 20.9% |
| Physical (injury) | 627 | 11.8% |
| Physical (death) | 615 | 11.6% |
| Environmental | 105 | 2.0% |
| Other | 33 | 0.6% |

## Autonomy level

| Level | Events | Share |
|---|---|---|
| High-action autonomy (human-out-of-the-loop) | 1901 | 35.8% |
| (empty) | 1594 | 30.0% |
| No-action autonomy (human support) | 764 | 14.4% |
| Low-action autonomy (human-in-the-loop) | 739 | 13.9% |
| Medium-action autonomy (human-on-the-loop) | 311 | 5.9% |

## Languages (events with at least one article in it), top 10

| Language | Events |
|---|---|
| eng | 2907 |
| zho | 977 |
| spa | 853 |
| por | 591 |
| fra | 493 |
| deu | 430 |
| kor | 371 |
| ara | 341 |
| tur | 311 |
| ell | 303 |

## Notes

- The severity field (`most_severe_harm`) is filled for 0 of 5309 events. This is the gap the project looks at.
- 300 events mention agents (rough keyword rule, not checked by hand yet).
