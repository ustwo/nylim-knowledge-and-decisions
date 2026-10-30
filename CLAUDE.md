# {{Product}} docs

The product's decisions, open questions, PRD, architecture overview, hypotheses, findings and success measures live in `docs/`. The repo is their source of truth, and people and agents both query it. [`docs/README.md`](docs/README.md) holds the full rules, and [`docs/scales.md`](docs/scales.md) defines every score; this is the short form.

## Answering questions about the project
- **Start with the generated views** in `docs/_generated/`: `evidence.md` for what the evidence says, `by-stage.md` and `by-objective.md` for one part of the product, `findings.md` for one frame, `timeline.md` for what changed when, and `index.json` for all of it. Then open the files they point to.
- **Cite by ID** in every answer, and say how settled each thing is: a decision's status, a hypothesis's verdict and strength, a finding's trust.
- **The views are computed.** Never edit `docs/_generated/`, and never write a computed value (strength, verdict, computed impact, seed) into a source file. Run `python scripts/evidence.py` to refresh them.

## Decisions
- **One file each,** in `docs/decisions/<kind>/<ID>.md`, in a folder for whoever makes the call: `product/` (PRD), `design/` (DES), `tech/` (TECH) and `business/` (BIZ). Start from `docs/decisions/_template.md`.
- **The kind is who makes the final call,** not the topic. One question is one decision with one owner; anyone else who had to agree goes in `agreed_with`. Never split a question into two decisions.
- **The title is the question.** The body has a Decision (the answer first, in bold), a Why (with the rejected alternatives), a "What this means for design and the build" section when it changes what someone should make, and an optional "Revisit when".
- **Depth follows the stakes.** Keep everyday decisions short. One that's hard to undo, such as architecture, the business model, process, or anything with legal, security or money risk, adds Drivers, Alternatives with pros and cons, and Consequences.
- **Take the next free number** for the prefix, and never reuse one.
- **Don't rewrite a decision.** A new decision supersedes it: set `supersedes` and `superseded_by` on both, change the old one's status, and note at its top what changed.
- **Don't reopen a decision** because of a new angle alone. If it has a "Revisit when", say whether that has happened.
- **Keep the index in step:** `docs/decisions/README.md` lists every decision with its status.
- **Cite decisions by ID** where the reason is a real choice someone might undo.
- **Optional fields** tie a decision in: `moves` (OBJ or KPI IDs), `stage`, `gate`, and `links` to what it rests on (`depends` for hypotheses and decisions; `supports`, `contradicts` or `mixed` for findings). Impact is computed from them. Set `impact` by hand only to raise it, with an `impact_reason`. Impact 4 or 5 needs Drivers, Alternatives and Consequences.
- Adding a link or tag to an existing decision is an edit, not a supersede.
- **The docs are client-facing.** A decision states what was decided and why, with no competitor names, internal discussion, or commercial or personal context.

## Open questions
- An open question is a decision with status `open`, with an `owner` and, when something waits on it, a `needed_by` date. There's no separate log.
- When it's answered, write the answer into the same file, set the status to `accepted` and the date to today, and update the lines that cite it.

## The PRD and the architecture overview
- `docs/prd/`, one file per section, opening with the current direction in its README. `docs/architecture.md` is the same for the system.
- Every statement is one line, a label (Decided, Proposed, Open, Out, Hypothesis) and an ID. A Hypothesis cites its HYP ID. Neither restates what it cites. A Hypothesis line with no ID yet is a draft: suggest logging it.
- Each PRD change adds a row to the change log in `docs/prd/README.md`. A change to the system's shape updates `docs/architecture.md` in the same change.
- Weigh new ideas and requests against the current direction. Point out when they'd change a bet, rather than adding them beside it.

## Build plans and specs
- They're engineering's, outside `docs/`. A plan cites the PRD capabilities and decisions it implements, and its acceptance criteria cite decision IDs.
- **A plan doesn't decide.** When planning makes a choice someone might undo, propose it as a decision, and have the plan cite it. Open questions found while building become open decisions.

## Success, stages and gates
- `docs/success.md`: goals in prose; objectives (OBJ) with a rank (north-star, primary, secondary, tertiary); KPIs (KPI), each naming its objective. Objectives are BIZ decisions and KPIs are PRD decisions, and each row cites one. Never add or change a row without its decision.
- `docs/gates.md`: the four stages (activate, motivate, sustain, change) and the project's gates. Tagging is optional, and a gate implies its stage. Don't push people to tag.

## Hypotheses
- `docs/hypotheses/`, one file each, HYP-01 onwards. A belief someone holds and hasn't proven, including a client's stated priority.
- `held_by` is `client` or `ustwo`, never a name. `stated_confidence` (1 to 5) is where the holder began. Change it only when they change their mind.
- The evidence on a hypothesis is computed. When it disagrees with the holder, say "the evidence has moved," never "this is wrong."
- Only the holder retires a hypothesis.

## Findings and sources
- `docs/sources.md` registers every source with an SRC ID. Sources stay where they live. Read them in place, through whatever connector reaches them, and never copy them into the repo.
- `docs/findings/`, one claim per file, FND-001 onwards. Every finding cites at least one SRC ID, has a `trust` from 1 to 5 on the scale in `docs/scales.md`, and an `evidence` type. Frames, stage, gate and `moves` are optional.
- **Trust is about the evidence.** 1: someone said it and we can't check it. 2: one source with a visible method. 3: a consistent pattern across independent sources, or across a well-run study's participants. 4: underlying data we can check, and enough of it. 5: system-of-record data at scale. Independent means not drawing on the same original.
- **Beliefs aren't findings.** What someone thinks matters or will work is a hypothesis. A client telling us what *is* happening is a finding at trust 1, type `stakeholder`.
- A finding links to what it bears on, with a stance. One that links to nothing is a seed: same file, same ID. Seeds are worked out by the script, never marked by hand.
- **Links live on whichever item came second.** Link to what already exists, and don't edit an older file just to add a back-link.
- Analytics: one finding per reading, with a `measurement` block naming its KPI. The export stays where it is.
- No participant names, recordings or transcripts in the repo: use codes such as P04, and short quotes.

## Drawing findings from a source
When asked to review a document, a deck, notes or an export:
1. Register it in `docs/sources.md` with the next SRC ID, if it isn't there.
2. Read the open decisions, active hypotheses, objectives and KPIs first, so you know what the project is asking.
3. Draft findings for claims that bear on those, linked with a stance. Draft seeds for anything strong or surprising that fits nothing yet. Don't pull out every claim.
4. Before writing each one, check `docs/_generated/findings.md` for the same claim. If it's there, add the new source to the existing finding and reconsider its trust, rather than writing a duplicate.
5. Suggest the trust score with a one-line reason, and put beliefs forward as hypotheses, not findings.
6. Mark every draft `drafted_by: agent` and `reviewed: false`. A person reviews the batch, sets `reviewed: true`, and it lands as one commit.
7. Run `python scripts/evidence.py`, and report anything that's moved: new entries on Needs a response, and any decision now resting on contradicted evidence.

When reviewing seeds, suggest the hypothesis or decision each one points to, or that it be archived.

## Ownership and changes
- Product ({{name}}) owns the PRD, the PRD decisions and the KPIs. Business ({{name}}, with NYLIM) owns the BIZ decisions and the objectives. Design ({{name}}) owns the DES decisions. Tech ({{name}}) owns the TECH decisions and the architecture overview. Strategy ({{name}}) reviews findings, logs hypotheses, and keeps sources and gates, and can draft objectives and KPIs.
- Docs changes go {{straight to main / through a pull request approved by …}}.
- **Propose before logging.** Don't add or change a decision until its owner agrees. Capture ideas elsewhere freely, but a proposal gets an ID only when it's in the repo.
- A commit that changes what design or the build should do ends with a "What this means for design and the build" section. When catching up on docs changes, start there, and check every decision it names.

## At the end of a session
Suggest:
- any decisions, open questions, hypotheses or findings to log, with the next free ID for each
- any PRD or architecture lines whose label should change, and any Hypothesis lines with no HYP ID yet
- whether the current direction has moved
- anything new on Needs a response, and any seed that now has something to link to
- running `python scripts/evidence.py` if the views are out of date
