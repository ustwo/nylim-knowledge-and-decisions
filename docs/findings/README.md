# Findings

What we've learned, one claim per file, each citing the sources it came from. Findings don't decide anything. They're the evidence that hypotheses and decisions rest on.

The index of every finding, grouped by frame, is generated: [`../_generated/findings.md`](../_generated/findings.md).

## Three layers

| Layer | What it is | Where it lives |
|---|---|---|
| **Sources** | The raw material: decks, notes, transcripts, reports, analytics exports | Where it already lives (Drive, Miro, Notion and so on), registered with an ID in [`sources.md`](../sources.md). Never copied into the repo |
| **Findings** | Claims drawn from sources that a decision, hypothesis, KPI or objective links to | Here, one file each |
| **Seeds** | Strong or surprising claims that nothing links to yet | Here too, with the same kind of ID. The script works out which findings are seeds |

## What makes a finding

- **One claim, in one sentence,** as its title. "Most advisers start with search," not "Search behaviour."
- **At least one source,** cited by its SRC ID. A finding with no source isn't a finding.
- **A trust score** from 1 to 5, on the scale in [scales](../scales.md#trust-how-far-we-can-rely-on-a-finding).
- **An evidence type:** `analytics`, `survey`, `test` (concept or usability testing), `interview`, `stakeholder` (what the client told us), `desk` (published reports and articles) or `audit` (our review of a product or service).
- **Optionally, frames:** `user`, `product`, `business` (the client's organisation) or `market`.
- **Optionally, where it sits:** an engagement-loop `stage` and `gate` (see [gates](../gates.md)), and the objectives or KPIs it `moves` (see [success](../success.md)).
- **Links** to the hypotheses and decisions it bears on, each with a stance: `supports`, `contradicts` or `mixed`.

A belief about what matters or what will work isn't a finding, even when the client says it. It's a [hypothesis](../hypotheses/README.md), `held_by: client`. A client telling us what *is* happening is a finding at trust 1, evidence type `stakeholder`.

## Getting findings from a source

Most findings arrive in a batch from one source, with AI doing the first pass.

1. **Register the source** in [`sources.md`](../sources.md) with the next SRC ID. The source stays where it lives.
2. **The AI reads it in place** and drafts findings. It looks for claims that bear on the current open decisions, hypotheses, objectives and KPIs. Those become findings, linked to what they bear on. It also flags anything strong or surprising that fits nothing yet. Those become seeds. It doesn't pull out every claim in the document.
3. **Check for repeats.** When a draft makes the same claim as an existing finding, add the new source to that finding instead, and reconsider its trust. A second independent source can lift it.
4. **Drafts are marked** `drafted_by: agent` and `reviewed: false`.
5. **A person reviews the batch** ({{likely Strategy}}): edits, adds, deletes, and sets `reviewed: true`. The batch lands as one commit, such as `docs(findings): add FND-012 to FND-019 from SRC-04, the kickoff deck`.

A person can write findings by hand too, and the same rules apply: one claim, a source, and a trust score.

Analytics work the same way. The measurement goes in as a finding with a `measurement` block, citing the KPI it measures, and the export stays where it is. Each new period is a new finding, so the history sits next to the baseline.

## Seeds

A seed is a finding nothing links to yet. It's the same file and the same ID. The script works out which findings are seeds and lists them in [`../_generated/seeds.md`](../_generated/seeds.md).

Seeds matter because they're the evidence that doesn't fit what we already believe. A seed usually means a hypothesis or decision is waiting to be written. Review them with the weekly decision review. Each seed either:

- **sparks a hypothesis,** which links to it,
- **earns a link** to an existing hypothesis, decision, KPI or objective, or
- **gets archived:** set `status: archived`. It stays in the repo, out of the default views.

The script flags seeds that have waited more than 30 days.

## Contradictions

Findings aren't rewritten when newer evidence disagrees. A newer finding links to the older one with `stance: contradicts`, and both stay. When the old finding is simply wrong (a misread number, say), archive it and say why at its top.

## Keep people out of the repo

Use participant codes, such as P04, never names. Keep quotes short. Recordings, transcripts and notes stay in the research tool, registered in [`sources.md`](../sources.md) as internal.

Findings may name public companies when the claim is about them, such as a published report. Leave out commercial-in-confidence and personal context, as for decisions.
