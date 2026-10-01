# Codebook v0 (draft, 2026-10-01)

This is the first draft of the rules we use to put one AIM event on the OECD
severity ladder. It will change after the first hand-coding round. Every
change gets a new version and a line in CHANGELOG.md.

## The ladder

From the OECD reporting framework (2025, criterion 10 "Severity", mandatory):
hazard; serious hazard; incident; serious incident; disaster; other.

The definitions below are quoted from OECD (2024), "Defining AI incidents and
related terms", OECD Artificial Intelligence Papers, pp. 11-14 (CC BY 4.0).

| Rung | OECD definition (short) | Actual or plausible harm? |
|---|---|---|
| 1. AI hazard | event where an AI system "could plausibly lead to an AI incident" | plausible |
| 2. Serious AI hazard | event where an AI system "could plausibly lead to a serious AI incident or AI disaster" | plausible |
| 3. AI incident | event where an AI system "directly or indirectly leads to" harm (a) health, (b) critical infrastructure, (c) human rights or legal obligations, (d) property, communities or environment | actual |
| 4. Serious AI incident | same, but "the death of a person or serious harm to the health", "serious and irreversible disruption" of critical infrastructure, "serious violation of human rights", "serious harm to property, communities or the environment" | actual |
| 5. AI disaster | "a serious AI incident that disrupts the functioning of a community or a society and that may test or exceed its capacity to cope" | actual |

The OECD itself says: "Assessing the seriousness of an AI incident ... is
context-dependent and is also left for further discussion" (2024, p. 15). So
the rules below are our own working choices, not OECD rules. We write them
down so other people can check them and disagree with them.

## Decision rules (v0)

Step 1. Actual or plausible harm?
- Harm already happened to someone (a person, a group, a firm, a right) -> go to Step 2.
- Harm is only possible, a warning, a test, a lab result, a policy debate -> go to Step 3.
- No AI system is involved, or the event is only an opinion piece -> code "out of scope".

Step 2. Which actual rung?
- Disaster: a community or society cannot function normally and needs outside help. Expect almost none.
- Serious incident if at least one is true:
  - someone died, or had serious health harm (hospital, lasting injury, suicide);
  - critical infrastructure stopped and it was not easy to reverse;
  - a serious rights violation: many people affected, or a protected group targeted, or a court or regulator found a breach;
  - large harm to property or communities (we use a working line of 1 million USD or more, or a whole town or sector affected; this line is our choice and will be tested).
- Otherwise: incident.

Step 3. Which plausible rung?
- Serious hazard: the plausible harm, if it happened, would be a serious incident by Step 2.
- Otherwise: hazard.

## Severity factors (from the 2026 due diligence guidance)

The OECD Due Diligence Guidance for Responsible AI (February 2026, Table 2.3)
says: "Severity of impacts will be judged by their scale, scope and
irremediable character", and "Severity is not an absolute concept and it is
context specific." So, besides the rung, the coder also gives each factor:

- Scale (how grave the harm is): low / medium / high / unclear.
- Scope (how many people or how wide): one person / a group / many people or a whole sector / unclear.
- Irremediability (can it be undone?): yes, easily / partly / no / unclear.

This lets us test one thing: does a rung built from the three factors agree
better between coders than one overall rung? The factors come from OECD
business guidance, not from the incident papers, so using them for incidents
is our own choice.

## Extra fields (from the 2025 framework)

- Multiple AI systems interacting (criterion 24): yes / no / unclear.
- Autonomy level (criterion 26): we copy AIM's value and add our own: none, low, medium, high, unclear.
- Confidence of the coder: low / medium / high.
- One-line reason, citing the rule used (e.g. "Step 2, death").

## Inputs the coder sees

Only what AIM itself holds: title, summary, AIM's rationales, article titles,
publishers and language counts. No outside search. This keeps the question
clear: what can be judged from the information AIM has.

## Open problems to test in round 1

- Incident vs serious incident for non-physical harm (rights, psychological, economic) will be the hard line.
- Many "hazard" events are opinion or policy news. Do they belong on the ladder at all?
- Repeated small harms adding up (the OECD notes this, p. 12): how to code a series?
