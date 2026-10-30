---
id: FND-000
title: "The claim, in one sentence"
status: active
date: YYYY-MM-DD
observed: YYYY-MM-DD
sources: [SRC-01]
evidence: interview
trust: 2
frames: [user]
stage: motivate
gate: G1
moves: [KPI-01]
links:
  - {id: HYP-01, stance: supports}
measurement:
  kpi: KPI-01
  value: "41%"
  period: 2026-Q3
  segment: "All visitors"
drafted_by: person
reviewed: true
---

<!--
Copy this file into findings/, named by its ID, with the next three-digit number for FND, such as FND-014.md.
- status: active or archived.
- date: the day it was logged. observed: when the evidence was gathered, as a date, month or quarter.
- sources: the SRC IDs from sources.md it came from. At least one.
- evidence: analytics, survey, test, interview, stakeholder, desk or audit.
- trust: 1 to 5, on the scale in ../scales.md.
- frames: any of user, product, business, market. Optional.
- stage and gate: optional, from ../gates.md. A gate implies its stage.
- moves: the OBJ or KPI IDs it bears on, from ../success.md. Optional.
- links: the hypotheses and decisions it bears on, each with a stance: supports, contradicts or mixed. Leave it empty for a seed.
- measurement: analytics only. Delete the block otherwise.
- drafted_by: agent or person. reviewed: true once a person has checked it.
Delete any optional line you don't use, then delete this comment.
-->

# The claim, in one sentence

## What we saw

The evidence: what people did or said, with short quotes attributed to participant codes such as P04, or the numbers and where they come from. Say how often it came up.

## What it doesn't tell us

The limits: who wasn't included, what wasn't asked, or what this could be confused with.
