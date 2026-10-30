---
id: PRD-00
title: "The question, as someone would ask it?"
kind: product
status: proposed
date: YYYY-MM-DD
agreed_with: []
supersedes: []
moves: [KPI-01]
stage: motivate
gate: G1
links:
  - {id: HYP-01, stance: depends}
  - {id: FND-001, stance: supports}
---

<!--
Copy this file into the folder for its kind, named by its ID, such as product/PRD-06.md.
- kind: whoever makes the final call: product, design, tech or business.
- status: accepted, proposed, open, parked, superseded or partly-superseded.
- agreed_with: anyone else who had to say yes, such as [Design, Tech]. Delete the line if none.
- supersedes: the IDs this replaces. Delete the line if none.
- An open question also takes owner and needed_by, and its Decision starts "Not decided yet."
- moves, stage and gate: optional. The objectives or KPIs it bears on (from ../success.md), and where it sits (from ../gates.md). Its impact is computed from moves.
- impact and impact_reason: only when the cost of being wrong is higher than what it moves suggests. Add both lines, or neither. Impact 4 or 5 needs the sections at the bottom.
- links: optional. The hypotheses or decisions it rests on (depends), and any findings behind it (supports, contradicts or mixed). Cite them in Why as well.
- Hard to undo, or impact 4 or 5? Add the sections at the bottom. Otherwise delete them.
Then add a row to the index in README.md, and delete this comment.
-->

# The question, as someone would ask it?

## Decision

**The answer, in a sentence or two.**

- One detail per bullet, when the answer needs detail.

This partly supersedes PRD-00, which {{said what}}. Everything else in PRD-00 stands.

## Why

The reasons, in plain sentences. Cite the decisions and hypotheses this depends on, and any findings behind it, by ID (HYP-03, FND-017). List the same IDs in `links`, so the evidence view can see them.

- Rejected: {{an alternative}}. {{Why it lost.}}
- Rejected: {{another}}. {{Why it lost.}}

## What this means for design and the build

- {{What someone should make or change. Delete this section if nothing changes.}}

## Revisit when

- {{What would reopen this, such as "after the first round of testing". Delete this section if nothing would.}}

<!-- For a decision that's hard to undo, add these, and move the Rejected lines into Alternatives. Otherwise delete them. -->

## Drivers

- {{What the decision had to satisfy.}}

## Alternatives

### {{Option}}: selected

**Pros:** {{…}} **Cons:** {{…}}

### {{Option}}

**Pros:** {{…}} **Cons:** {{…}} Rejected because {{…}}.

## Consequences

- **Benefits:** {{…}}
- **Risks:** {{…}}
- **Mitigations:** {{how each risk is handled}}
