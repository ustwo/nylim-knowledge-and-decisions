---
id: HYP-00
title: "A statement that could turn out wrong"
status: active
date: YYYY-MM-DD
held_by: client
stated_confidence: 3
moves: [OBJ-01]
stage: motivate
gate: G1
links:
  - {id: HYP-00, stance: depends}
supersedes: []
---

<!--
Copy this file into hypotheses/, named by its ID, with the next two-digit number for HYP, such as HYP-05.md.
- status: active, retired or superseded.
- held_by: client or ustwo. A side, never a name.
- stated_confidence: 1 to 5, how strongly the holder believes it now. See ../scales.md.
- moves: the OBJ or KPI IDs it bears on. Its impact is computed from these.
- impact and impact_reason: only when the cost of being wrong is higher than what it moves suggests. Add both lines, or neither.
- stage and gate: optional, from ../gates.md.
- links: other hypotheses it depends on (depends), or findings logged before it (supports, contradicts or mixed).
- supersedes: the IDs this replaces. Delete the line if none.
Delete any optional line you don't use, then delete this comment.
-->

# A statement that could turn out wrong

## What we believe

The belief in a sentence or two, and where it came from: who said it, in which source, or what led us to it.

## Why it matters

What would change if it's wrong: the decisions or plans that rest on it.

## What would show it's wrong

The evidence that would change the holder's mind, such as "fewer than half of testers start with search." This is what a study or a KPI should look for.
