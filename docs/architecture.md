# {{Product}} architecture overview

*Updated YYYY-MM-DD · Owner: {{name}}*

What the system is right now: its parts, what each owns, how data flows, and the rules that keep it coherent. It's tech's version of the PRD. Each line cites the TECH decision behind it and never restates it. A line with no decision behind it is a **Hypothesis**, citing its HYP ID.

A change that alters the system's shape updates this page in the same change.

## What it is

{{One or two sentences: what the system is, who uses it, and what it sits inside, such as a host app or a client's platform.}}

## The parts

| Part | What it owns | Built with | Label |
|---|---|---|---|
| {{e.g. The app}} | {{…}} | {{…}} | **Decided** · TECH-01 |
| {{e.g. The API}} | {{…}} | {{…}} | **Hypothesis** · {{HYP-ID}} |
| {{e.g. The content system}} | {{…}} | {{…}} | **Open** · {{ID}} |

## How data flows

{{The main paths, one line each, such as: the app asks the API, the API reads the database, content is baked in at build time. A diagram can go here once the shape settles.}}

## Rules that keep it coherent

The constraints every change has to respect, each with the decision that set it.

| Rule | Label |
|---|---|
| {{e.g. The app never talks to the database directly}} | **Decided** · {{ID}} |

## Where it runs

| Environment | Where | Who owns it | Label |
|---|---|---|---|
| Development | {{…}} | {{…}} | **Decided** · TECH-01 |
| Production | {{…}} | NYLIM | **Open** · TECH-02 |
