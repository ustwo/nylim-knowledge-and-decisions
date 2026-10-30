# Pedal: a worked example

A small, made-up project that shows the fork working end to end. Pedal is a city bike-share app in beta. Only the parts the script reads are here: decisions, hypotheses, findings, sources, success measures and gates.

Run the script on it from the repo's root:

```sh
python scripts/evidence.py --root example
```

Then read [`docs/_generated/evidence.md`](docs/_generated/evidence.md). Things to notice:

- **HYP-01**, the client's belief that riders pay after three rides, is held at starting confidence 5, and two strong findings contradict it. It tops Needs a response, and **PRD-01**, which rests on it, is flagged too.
- **HYP-02** is supported by analytics and a review of support tickets, so it's on Build on.
- **HYP-03** has only the client's say-so behind it, a trust-1 finding, so it's high on Test next.
- **HYP-04** inherits impact 5 from the north-star objective it moves, so it tops Test next.
- **FND-007** links to nothing, so it's a [seed](docs/_generated/seeds.md).
- **FND-009** is an AI draft nobody has reviewed yet, so it isn't counted, and the script warns about it.
- **KPI-03** has two readings, before and after DES-01 shipped, in the [view by objective](docs/_generated/by-objective.md).
- The [view by stage](docs/_generated/by-stage.md) gathers everything about gate G3, choosing a plan.
