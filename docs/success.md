# What success looks like

What {{Product}} is trying to achieve, and how we'll know. Goals are written in prose. Objectives and KPIs each have an ID, and every KPI names the objective it ladders into. Decisions, hypotheses and findings tag the ones they `move`, and the script uses those tags to work out impact and to build the [view by objective](_generated/by-objective.md).

- **Goals** are the overarching ambitions. They don't need IDs.
- **Objectives** are the outcomes we're targeting, specific enough to measure. Each belongs to a goal, and has a rank: `north-star`, `primary`, `secondary` or `tertiary`. The rank sets the impact of anything that moves it.
- **KPIs** are how we measure progress towards an objective. One objective usually has one or two. When one measure feeds several objectives, write a narrower KPI for each.

**Who decides:** objectives are business calls, {{name}} with NYLIM, recorded as BIZ decisions. KPIs are product calls, {{name}}, recorded as PRD decisions. Strategy can draft both. This page points to those decisions and never argues for itself: adding or changing an objective or KPI goes through a decision, and its Label cites it.

## Goals

### {{Goal A: the ambition, in a few words}}

{{A short paragraph: what it is, and why it matters to NYLIM.}}

### {{Goal B}}

{{…}}

## Objectives

| ID | Objective | Goal | Rank | Stage | Gate | Label |
|---|---|---|---|---|---|---|
| OBJ-01 | {{The outcome, specific enough to measure}} | {{Goal A}} | {{north-star / primary / secondary / tertiary}} | | | **Open** · BIZ-01 |
| OBJ-02 | {{…}} | {{Goal A}} | {{…}} | | | **Open** · BIZ-01 |

Stage and Gate are optional, from [gates](gates.md).

## KPIs

| ID | KPI | Objective | Baseline | Target | Readiness | Stage | Gate | Label |
|---|---|---|---|---|---|---|---|---|
| KPI-01 | {{What's measured, and how}} | OBJ-01 | {{value, and when}} | {{value, and by when}} | {{track now}} | | | **Open** · PRD-05 |
| KPI-02 | {{…}} | OBJ-02 | {{…}} | {{…}} | {{tag in build}} | | | **Open** · PRD-05 |

**Readiness** says whether we can measure it yet: `track now` (the data exists), `tag in build` (it needs tracking added), `needs data join` (it needs data from more than one system) or `survey or research` (it isn't in any system).

Measurements over time are findings with a `measurement` block, so each KPI's history builds up in the [view by objective](_generated/by-objective.md), next to its baseline.

## Guardrails

{{Optional. What must not get worse while we chase these, such as complaint rates or compliance checks. Each one as a line with its label.}}
