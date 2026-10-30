# NYLIM knowledge and decisions

The source of truth for ustwo's work with NYLIM: decisions, open questions, the PRD, hypotheses, findings and success measures, as plain Markdown that people and agents can both read, cite and query.

It's built on a fork of Zac's [product docs template](FORK.md#where-it-came-from), trying out an evidence layer on a live project. Its core rules are unchanged. [`FORK.md`](FORK.md) lists what's been added, so the parts that work can be pulled back into the original.

## What's here

| Path | What it is |
|---|---|
| [`docs/README.md`](docs/README.md) | How the docs work: who owns what, how changes land, how to write each kind of file |
| [`docs/scales.md`](docs/scales.md) | The three five-point scales (trust, starting confidence, impact) and what the script works out from them |
| [`docs/decisions/`](docs/decisions/README.md) | Every decision, one file each, in a folder for whoever makes the call. An open question is a decision with status `open` |
| [`docs/hypotheses/`](docs/hypotheses/README.md) | What someone believes and hasn't proven, including a client's stated priorities, one file each |
| [`docs/findings/`](docs/findings/README.md) | Claims drawn from sources, one file each, with a trust score. A finding nothing links to yet is a seed |
| [`docs/sources.md`](docs/sources.md) | Every source, with an ID. Sources stay where they live |
| [`docs/success.md`](docs/success.md) | Goals, and the objectives and KPIs that measure them, with IDs |
| [`docs/gates.md`](docs/gates.md) | The engagement loop's four stages, and the project's gates. Optional tags |
| [`docs/prd/`](docs/prd/README.md) | The PRD, one file per section, opening with the current direction. Each statement cites the decision or hypothesis behind it |
| [`docs/architecture.md`](docs/architecture.md) | Tech's version of the PRD |
| [`docs/studies/`](docs/studies/README.md) | Planned research, when it's worth planning. Optional |
| [`docs/_generated/`](docs/_generated/README.md) | The evidence views, worked out by the script. Never edited by hand |
| [`scripts/evidence.py`](scripts/evidence.py) | Checks the docs, works out the evidence, and writes the views |
| [`example/`](example/README.md) | A small made-up project, to see it all working |
| [`CLAUDE.md`](CLAUDE.md) | The same rules, for agents working in the repo |
| [`.gitmessage`](.gitmessage) | A commit template with the "What this means for design and the build" section |

## See it work

```sh
pip install -r scripts/requirements.txt
python scripts/evidence.py --root example
```

It needs Python 3.9 or later. Then open [`example/docs/_generated/evidence.md`](example/docs/_generated/evidence.md). The [example's README](example/README.md) says what to look for.

## Starting a project

1. Delete `example/` once the team has looked at it.
2. Search for `{{` and fill in each placeholder: the product's name, who owns what, and how changes land. NYLIM is already filled in as the client.
3. Check the kinds of decision: product (PRD), design (DES), tech (TECH) and business (BIZ). Drop or add a kind to match who makes calls on the project.
4. Go through the starter questions in `docs/decisions/`. Keep the ones that apply, and delete the rest.
5. Register the sources you've been given in `docs/sources.md`.
6. Write the first current direction at the top of `docs/prd/README.md`, even if every bet is an early hunch.
7. Turn on the commit template: `git config commit.template .gitmessage`.
8. On GitHub, set **Settings → Actions → General → Workflow permissions** to "Read and write", so the views regenerate on every push to `main`.

### How much to use

Not every project needs every part. Use what earns its keep.

| Tier | What it uses |
|---|---|
| **Every project** | Decisions, open questions, the PRD and sources. The original template |
| **Most projects** | Findings, with a trust score and a link to what they bear on. AI does most of the work |
| **Bigger projects** | Hypotheses, objectives and KPIs, analytics as measurements, and stage and gate tags |

Impact mostly fills itself in from the objective something moves, so it costs nothing unless you want to raise it. If a small project only ever uses the first tier, that's still a win. The script runs happily on whatever's there.

## The idea in short

The original template's ideas all still hold:

- **A decision is a question with an answer and a reason.** Each is a file named by its ID, so anything can cite it.
- **A decision belongs to whoever makes the call.** One question, one decision, one owner.
- **Decisions aren't rewritten.** A new one supersedes an old one, and both stay.
- **A decision can say what would reopen it.** Until that happens, a new angle isn't enough.
- **Open questions are decisions waiting for an answer,** not a separate log.
- **The PRD is the current picture, and the decisions are the reasons.** The PRD cites them in one line and never restates them.
- **A change says what it means for design and the build.**

This fork adds:

- **Findings come from anywhere.** Drop in any source, and AI drafts the findings, one claim each, for a person to review. Only findings come into the repo.
- **Hypotheses get IDs,** including the client's priorities, with who holds them and how strongly.
- **Everything links up:** source → finding → hypothesis → decision → KPI → objective. Confidence flows down the chain, and impact flows up it.
- **Judge at the edges, compute the rest.** People set trust, starting confidence and objective rank. The script works out the evidence on every hypothesis and decision, and what needs a response, what to test next, and what to build on.
- **Seeds are kept.** Evidence that fits nothing yet is often what prompts the next hypothesis.
- **Tags are optional.** Stage, gate, frame and objective help you zero in, and nobody is forced to use them.
