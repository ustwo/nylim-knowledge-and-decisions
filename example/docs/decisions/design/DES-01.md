---
id: DES-01
title: "What happens when an unlock fails?"
kind: design
status: accepted
date: 2026-10-12
gate: G2
moves: [KPI-03]
links:
  - {id: HYP-02, stance: depends}
  - {id: FND-001, stance: supports}
---

# What happens when an unlock fails?

## Decision

**The app retries once on its own, then offers the nearest working bike with directions.**

## Why

A failed first unlock costs us the rider (HYP-02), and one in five first unlocks fails (FND-001).

- Rejected: an error message with a support link. It leaves the rider stranded at the dock.

## What this means for design and the build

- Add an automatic retry, and a "nearest working bike" screen.
