---
id: PRD-01
title: "Which plan do new riders see first?"
kind: product
status: accepted
date: 2026-10-08
agreed_with: [Design]
moves: [OBJ-02]
gate: G3
links:
  - {id: HYP-01, stance: depends}
---

# Which plan do new riders see first?

## Decision

**Pay as you go first, with the monthly plan offered after a rider's third ride.**

## Why

The client expects riders to pay once they've taken a few rides (HYP-01), so the offer waits until then.

- Rejected: offering every plan at the first unlock. It adds a decision at the moment we most want people riding.

## What this means for design and the build

- The plan offer appears after the third completed ride, not at sign-up.

## Revisit when

- The beta shows when riders actually choose to pay.

## Drivers

- Don't add friction before the first ride.
- Paid-plan take-up is a primary objective (OBJ-02).

## Alternatives

### Pay as you go first, offer after three rides: selected

**Pros:** nothing in the way of the first ride. **Cons:** relies on HYP-01.

### All plans at the first unlock

**Pros:** catches riders when they're deciding. **Cons:** a slower first ride. Rejected because of the friction.

## Consequences

- **Benefits:** a faster first ride.
- **Risks:** if riders decide earlier, we offer the plan too late.
- **Mitigations:** KPI-02 is read weekly in the beta.
