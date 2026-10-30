# Hypotheses

What someone believes and hasn't proven: about the people we serve, what will work, or where the value is. One file each, with an ID such as HYP-04, so the PRD, decisions and findings can cite it.

A client's stated priority is a hypothesis too. "Cross-selling is our biggest lever" is a belief about where the value is, held by the client, and the evidence can bear it out or not.

What the evidence says about each hypothesis is worked out by the script and shown in [`../_generated/evidence.md`](../_generated/evidence.md). Nobody maintains it by hand.

## What makes a hypothesis

- **A statement that could turn out wrong,** as its title. "Advisers arrive knowing the fund they want," not "Adviser intent."
- **Who holds it,** as a side: `client` or `ustwo`. Never a person's name.
- **A starting confidence** from 1 to 5: how strongly the holder believed it when it was logged. See [scales](../scales.md#starting-confidence-how-strongly-a-hypothesis-is-held).
- **Optionally, what it moves:** the objectives or KPIs in [success](../success.md) it bears on. Its impact is computed from these. Set `impact` by hand, with an `impact_reason`, only when the cost of being wrong is higher than that.
- **Optionally, where it sits:** a `stage` and `gate` from [gates](../gates.md).
- **Links,** when it depends on another hypothesis (`stance: depends`), or when it was written after the findings that bear on it (`supports`, `contradicts` or `mixed`).

## Links live on whichever item came second

You only ever link to something that already exists:

- A new finding names the hypotheses it bears on.
- A hypothesis written after its evidence names those findings.
- A decision names the hypotheses it rests on.

Nobody edits an older file just to add a back-link. The script reads links in both directions. If the same pair is linked from both sides, the stances must match.

## Statuses

| Status | Means |
|---|---|
| `active` | Held, and counted in the evidence views |
| `retired` | No longer held. Say why at its top |
| `superseded` | Replaced by a better-worded or narrower hypothesis. Set `supersedes` and `superseded_by`, as for decisions |

A hypothesis isn't retired just because the evidence contradicts it. The holder retires it when they stop believing it. Until then, the contradiction is what the evidence view is for.

## Writing them for the client to read

The repo is shared with the client, so hypotheses read as rigour, not judgement:

- **Who holds it is a side, not a name:** "held by the client," never a person.
- **Starting confidence is where we began,** not a score for being right.
- **When the evidence disagrees,** the generated view says "the evidence has moved," not "this is wrong."

## In the PRD

A PRD line labeled **Hypothesis** cites its HYP ID instead of spelling the belief out: `**Hypothesis** · HYP-04`. The PRD's Hypothesis lines are then the list of things to test, ranked in [Test next](../_generated/evidence.md#test-next).
