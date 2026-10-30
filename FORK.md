# About this fork

## Where it came from

Forked from Zac's product docs template, to try an evidence layer on the NYL Design Ops project. It's an experiment, not a v2. Whatever works can be pulled back into the original, and anything can be edited or reverted once a project has tested it.

## What's unchanged

The core rules: decisions as questions with answers, one owner per decision by who makes the call, superseding instead of rewriting, "Revisit when", open questions as decisions, the PRD citing instead of restating, and the "What this means for design and the build" commit section.

## What's added or changed

Each change below stands on its own as far as possible, so they can be taken back one at a time.

| Change | Files | Depends on |
|---|---|---|
| **Sources get IDs** (SRC-01). Sources stay where they live, and findings cite them | `docs/sources.md` | Nothing |
| **Findings from any source,** one claim each, with a five-point trust score and an evidence type. Replaces `research/` and its RES IDs | `docs/findings/`, `docs/scales.md` | Source IDs |
| **Seeds:** findings nothing links to yet, kept and reviewed rather than discarded. Same record and ID, worked out by the script | `docs/findings/README.md` | Findings |
| **AI drafts, a person reviews:** `drafted_by` and `reviewed` on findings, and one commit per source | `docs/findings/`, `CLAUDE.md` | Findings |
| **Hypotheses get IDs** (HYP-01), including the client's stated priorities, with `held_by` and `stated_confidence`. PRD Hypothesis lines cite them | `docs/hypotheses/`, `docs/prd/` | Nothing |
| **Success measures:** goals in prose, objectives with a rank, and KPIs that each name an objective. Objectives are BIZ decisions and KPIs are PRD decisions. New starter question PRD-05, and BIZ-01 reworded | `docs/success.md`, `docs/decisions/` | Nothing |
| **Stages and gates:** activate, motivate, sustain and change, and the project's gates. Optional tags on anything | `docs/gates.md` | Nothing |
| **Links with a stance** (supports, contradicts, mixed, depends), stored on whichever item came second | Templates, `docs/README.md` | Findings, hypotheses |
| **Impact,** the cost of being wrong, computed from what something moves and what rests on it | `docs/scales.md` | Success measures, links |
| **The script and the views:** checks, evidence strength and verdict, the three lists, and views by frame, stage, objective and time | `scripts/`, `docs/_generated/`, `.github/workflows/docs.yml` | All of the above |
| **A worked example** | `example/` | The script |

## Still open

- **Thresholds.** The trust weights, the 70% and 30% verdict lines, and the list cut-offs in `scripts/config.yaml` are first guesses. Tune them after NYL.
- **The contradiction view is visible to the client.** The wording ("the evidence has moved") is meant to make that comfortable. Worth checking once it's real.
- **Strategy as a decision kind.** Strategy reviews findings, logs hypotheses and drafts success measures, but there's no STRAT kind of decision. Not needed so far.
- **The commit section** still says "What this means for design and the build." It may need to cover strategy and the business too.
