# How these docs work

{{Product}}'s decisions, open questions, PRD, architecture overview, hypotheses, findings and success measures live here, in the repo, as the source of truth. People add to it, and people and AI query it. This page says who owns each part, how they change, and how to write them.

The scores used throughout, and what the script works out from them, are in [scales](scales.md).

## Who owns what

| Docs | Owner | Who agrees a change |
|---|---|---|
| The PRD (`prd/`) | Product: {{name}} | {{name}} |
| The architecture overview (`architecture.md`) | Tech: {{name}} | {{name}} |
| Product decisions (PRD) | Product: {{name}} | {{name}}, with NYLIM where it changes scope |
| Business decisions (BIZ) | Product: {{name}} | NYLIM |
| Design decisions (DES) | Design: {{name}} | {{name}} |
| Tech decisions (TECH) | Tech: {{name}} | {{name}}, with {{client's tech contact}} where it touches their systems |
| Objectives (`success.md`) | Business: {{name}}, recorded as BIZ decisions | NYLIM |
| KPIs (`success.md`) | Product: {{name}}, recorded as PRD decisions | {{name}} |
| Hypotheses (`hypotheses/`) | Whoever holds them, client or ustwo. Logged by {{Strategy: name}} | Nobody needs to agree a hypothesis. It's a belief, not a commitment |
| Findings (`findings/`) | {{Strategy: name}}, who reviews each batch before it lands | {{name}} |
| Sources (`sources.md`) and stages and gates (`gates.md`) | {{Strategy: name}} | {{name}} |

Strategy can draft objectives and KPIs for their owners to agree.

Anyone can propose a decision or raise a question. The owner makes it `accepted`. A decision nobody moves past `proposed` isn't a decision yet, so owners review what's waiting on them each week. The same review is a good time to look at [seeds](findings/README.md#seeds) and the [Needs a response](_generated/evidence.md#needs-a-response) list.

## How changes land

Pick one route, write it here, and keep [`CLAUDE.md`](../CLAUDE.md) in step.

- **Straight to main.** Docs changes go to `main` without a pull request. This is fast, and it works when the owner makes or agrees each change as it happens. The commit message carries what the change means (see [Commits](#commits)).
- **A pull request the owner approves.** Each change goes on its own branch, apart from design or code work, with the owner as reviewer. New decisions stay `proposed` until it merges.

**This project uses: {{straight to main / a pull request approved by …}}.**

Design and code changes take their own route either way. Keep docs changes out of them, so each can be agreed on its own.

## Decisions

Each decision is one file: `decisions/<kind>/<ID>.md`. Copy [`decisions/_template.md`](decisions/_template.md) to start one.

### The kinds

| Kind | Prefix | Folder | Who makes the call | Usually about |
|---|---|---|---|---|
| Product | PRD | `product/` | Product | What {{Product}} does and for whom: capabilities, journeys, what each milestone shows |
| Design | DES | `design/` | Design | How it works, looks and feels: structure, flows, interaction, content, visual direction, any design system |
| Tech | TECH | `tech/` | Tech | How it's built and run: architecture, platforms, data, security, hosting, how the team builds |
| Business | BIZ | `business/` | The business, often the client | Who it serves, how it makes money, what it's measured by |

**A decision's kind is whoever makes the final call,** not what it's about. Most questions touch more than one discipline, so "is this product or design?" has no clean answer. "Who has to say yes?" does.

- "Every trade needs the person's approval" is a product call: PRD.
- "Approval is a slide, then a face scan" is a design call: DES. It cites the PRD decision.
- "Approvals are checked on the server, never only in the app" is a tech call: TECH.

One question is one decision, with one owner. When someone else has to agree, name them in `agreed_with` instead of writing a second decision.

### IDs

Take the next number for the prefix, with two digits: DES-01, DES-02, and so on. Check the folder first, since someone else may have just taken one. An ID is never reused, even when its decision is superseded.

### Fields

```yaml
---
id: PRD-07
title: "Does someone need an account before they can try it?"
kind: product
status: accepted
date: 2026-10-21
agreed_with: [Design, Tech]  # others who had to say yes, if any
supersedes: [PRD-03]         # only when it replaces an earlier decision
superseded_by: [PRD-12]      # only when a later decision replaces it
owner: "{{name}}"            # open questions only: who can answer it
needed_by: 2026-10-30        # open questions only
moves: [KPI-03]              # optional: the objectives or KPIs it bears on
stage: motivate              # optional: activate, motivate, sustain or change
gate: G2                     # optional: implies the stage
links:                       # optional: what it rests on
  - {id: HYP-04, stance: depends}
  - {id: FND-031, stance: supports}
impact: 5                    # optional: only to raise the computed impact
impact_reason: "Hard to reverse once advisers are migrated"
---
```

**The title is the question,** such as "Which tabs does the app have?", not "Tab bar". A question says what's being decided, and it still reads well once the answer changes.

**The date** is the day the decision took its current status. When an open question is answered, the date moves to that day.

**The optional fields** connect a decision to the rest of the picture. `moves`, `stage` and `gate` say what it bears on and where it sits, so it shows up in the [view by objective](_generated/by-objective.md) and the [view by stage](_generated/by-stage.md). `links` say what it rests on: the hypotheses and decisions it depends on, and the findings behind it. They let the script flag a decision when the evidence moves against something it rests on. Its impact is computed from `moves` and from what rests on it. Set `impact` by hand only to raise it, with a reason. See [scales](scales.md#impact-the-cost-of-being-wrong).

Adding or correcting a link or tag on an existing decision is an edit, like fixing a typo. It doesn't change what was decided.

### Statuses

| Status | Means |
|---|---|
| `accepted` | Agreed, and in force |
| `proposed` | Written up, waiting for its owner to agree |
| `open` | A question still to answer |
| `parked` | Deliberately set aside for now |
| `superseded` | Replaced by a later decision |
| `partly-superseded` | Some of it replaced by a later decision. The rest still holds |

### The body

Every decision has these sections:

- **Decision.** Lead with the answer, in bold, in a sentence or two. Then the detail: one idea per bullet.
- **Why.** The reasons, citing the [findings](findings/README.md) and [hypotheses](hypotheses/README.md) behind them by ID, such as FND-017 or HYP-04, and listing the same IDs in `links`. Then a "Rejected:" bullet for each alternative that was considered, and why it lost. The rejected options stop the same debate from starting again.
- **What this means for design and the build.** Only when it changes what someone should make. Say what to change, not how.
- **Revisit when.** Optional. What would reopen this decision, such as "after the first round of testing" or "if the platform adds native sign-in". Until that happens, a new angle on its own isn't a reason to reopen it.

### Depth follows the stakes

Most decisions are easy to undo, and should take minutes to write: the four sections above, kept short.

A decision that's **hard to undo** gets more. Architecture, the business model, how the team works, and anything with legal, security or money risk are examples. So is any decision at impact 4 or 5, and the script checks for these sections there. Add:

- **Drivers:** what the decision had to satisfy, in a few bullets.
- **Alternatives:** each option with its pros and cons, not just a "Rejected:" line.
- **Consequences:** the benefits, the risks, and how each risk is mitigated.

The file, the ID and the index are the same either way. Only the length changes.

Write it for the client to read:

- State what was decided and why. Leave out the internal discussion, commercial or personal context, and competitor names.
- Say who agreed it and when, if that matters later: "Agreed by {{client contact}} on Oct 23."
- Don't invent a reason. If the record has none, say so: "The record gives no reason beyond the approach itself."

### Superseding

A decision isn't rewritten when it changes. A new decision supersedes it, so an ID always means one thing, and everything that cites it stays true.

1. List the earlier ID in the new decision's `supersedes`, and say in its body what it replaces.
2. Add the new ID to the earlier decision's `superseded_by`, and set its status to `superseded` or `partly-superseded`.
3. At the top of the earlier decision, add a line saying what changed: `> Partly superseded by DES-14: search moves to the top of the screen.` Leave the rest of its text as it was.
4. Update the index, and any PRD or architecture lines that cite the earlier decision.

Fixing a typo or a broken link is an edit, not a supersede.

### Citing

Cite a decision by ID where the reason is a real choice someone might undo: in the PRD, the architecture overview, another decision, a build plan, a commit, or a code comment that explains why. Don't cite a decision for something nobody would question.

## Open questions

An open question is a decision with status `open`. There's no separate log.

- Its **Decision** section says "Not decided yet," and then what's known so far.
- Its **Why** section says why it matters and what it blocks.
- It names an `owner`, the person who can answer it, and a `needed_by` date when something waits on it.

When it's answered, write the answer into the same file and set its status to `accepted` and its date to the day it was answered. Then update the lines that cite it in the PRD and the architecture overview.

To see every open question, look for `status: open` in `decisions/`, or the open rows in the [index](decisions/README.md).

## The PRD

The PRD is in [`prd/`](prd/README.md), one file per section. It says what {{Product}} is, who it's for, what it does and what it doesn't do. Its README opens with the **current direction:** the few bets the team is making right now, and how settled they are.

Every statement carries a label saying how settled it is:

| Label | Means | Decision status |
|---|---|---|
| **Decided** | Agreed and recorded | `accepted` |
| **Proposed** | Written up, waiting for sign-off | `proposed` |
| **Open** | A question still to answer | `open` |
| **Out** | Deliberately not doing | `parked` or `superseded` |
| **Hypothesis** | Someone's working idea, not agreed or proven | none, but cites its HYP |

- **A statement with a decision behind it is one line, a label and an ID.** It never restates the decision's reasoning, so the two can't drift apart.
- **A statement with no decision behind it is a Hypothesis,** however confident it sounds, and it cites its [hypothesis](hypotheses/README.md) the same way: `**Hypothesis** · HYP-04`. While drafting, a Hypothesis can be written out without an ID, and the script lists it until it's logged.
- When the PRD changes, add a row to the change log in [`prd/README.md`](prd/README.md) and bump its version.

## The architecture overview

[`architecture.md`](architecture.md) is tech's version of the PRD: what the system is right now, meaning its parts, what each owns, how data flows, and the rules that keep it coherent. It follows the same rules as the PRD: each line cites the TECH decision or hypothesis behind it, and never restates it.

A change that alters the system's shape updates the overview in the same change, so the whole picture stays true as work lands piece by piece.

## Build plans and specs

How each piece gets built lives in engineering's build plans, outside these docs, in whatever form the team uses. A plan may hold a spec for each piece of work: its intent, acceptance criteria, non-goals and open questions. Where this meets the docs:

- **A plan cites, it doesn't decide.** A plan names the PRD capabilities and the decisions it implements. A choice made while planning that someone might later undo becomes a decision here, and the plan cites it.
- **Acceptance criteria cite decisions.** "Every buy asks for approval (PRD-02)" can be checked against the decision it comes from.
- **Open questions found while building** become open decisions here, with an owner, rather than a list in the plan.

## Success

[`success.md`](success.md) holds the goals, in prose, and the objectives and KPIs, each with an ID. Every KPI names the objective it ladders into, and each objective has a rank: north star, primary, secondary or tertiary.

- **It points to decisions.** Objectives are agreed as BIZ decisions and KPIs as PRD decisions, and each row's label cites one.
- **Anything can say what it moves.** A decision, hypothesis or finding tags the objectives or KPIs it bears on. That sets its impact, and puts it in the [view by objective](_generated/by-objective.md).
- **Measurements are findings.** A reading of a KPI, from analytics or a survey, is a finding with a `measurement` block. Its history builds up next to the baseline.

## Stages and gates

[`gates.md`](gates.md) lists the four stages of the engagement loop (activate, motivate, sustain and change) and the project's gates, each in one stage. Any item can be tagged with a stage or a gate. It's optional, and a gate implies its stage. The [view by stage](_generated/by-stage.md) gathers everything for one stage or gate.

## Hypotheses

A [hypothesis](hypotheses/README.md) is something someone believes and hasn't proven, including a client's stated priorities. One file each, with an HYP ID, saying who holds it (client or ustwo) and their starting confidence. The evidence on it is computed, never written in.

## Findings

A [finding](findings/README.md) is one claim drawn from one or more [sources](sources.md), with a trust score from 1 to 5. One file each, with an FND ID. It links to the hypotheses and decisions it bears on, with a stance: supports, contradicts or mixed. A finding nothing links to yet is a **seed**: same file, same ID. Seeds get reviewed, and each one sparks a hypothesis, earns a link, or is archived.

- **Findings don't decide.** They're evidence. The owner of a question decides it.
- **Most findings arrive in a batch from one source,** drafted by AI and reviewed by a person before they land as one commit. The workflow is in the [findings README](findings/README.md#getting-findings-from-a-source).
- **Studies are optional.** When research is worth planning, a [study](studies/README.md) names the hypotheses and questions it's for before it starts.

## The evidence views

[`scripts/evidence.py`](../scripts/evidence.py) reads every file, checks the links and scores, works out the evidence on each hypothesis and decision, and writes the views in [`_generated/`](_generated/README.md):

- [`evidence.md`](_generated/evidence.md): Needs a response, Test next, Build on, and the evidence for each hypothesis and decision
- [`seeds.md`](_generated/seeds.md): findings nothing links to yet
- [`findings.md`](_generated/findings.md): every finding, by frame
- [`by-stage.md`](_generated/by-stage.md) and [`by-objective.md`](_generated/by-objective.md): everything for one stage, gate or objective
- [`timeline.md`](_generated/timeline.md): what we learned and decided, newest first
- `index.json`: all of it, for agents

The views are regenerated on every push to `main` (see [`.github/workflows/docs.yml`](../.github/workflows/docs.yml)), or locally with `python scripts/evidence.py`. Never edit them by hand. How the evidence is worked out is in [scales](scales.md#what-the-script-works-out).

## Sources

[`sources.md`](sources.md) registers what the team was given and has gathered, such as briefs, decks, contracts, prototypes, research notes and analytics, each with an SRC ID, and what each one governs. Sources stay where they live, and only findings come into the repo. When two sources disagree, it says which wins. When a copy is kept here but the original lives elsewhere, it says where the original is. A source is an input: it becomes a commitment only through a decision.

## Commits

Docs commits follow the repo's commit style, such as `docs: record the answers from the kickoff`, `docs(decisions): accept PRD-02, the first journeys` or `docs(findings): add FND-012 to FND-019 from SRC-04`. The body says what changed and why.

**A commit that changes what design or the build should do ends with a section headed "What this means for design and the build"**, with a bullet for each change. [`.gitmessage`](../.gitmessage) sets it up. When catching up on docs changes, read those sections first, and check every decision they name.

## Working notes outside the repo

Explorations, meetings, workshops and drafts can live in the team's own notes. Keep them out of the repo, and follow these rules where they meet it:

- **A proposal gets an ID only when it's in the repo.** In notes, call it a proposal and describe it. Don't give it a number.
- **Propose before logging.** Agree a new or changed decision with its owner before writing it here.
- **At the end of a working session,** check for decisions, questions, hypotheses or findings to log, using the next free ID in the repo, and whether the current direction has moved.
