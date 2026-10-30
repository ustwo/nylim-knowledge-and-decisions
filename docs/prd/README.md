# {{Product}} PRD

*Version 0.1 · YYYY-MM-DD*

What {{Product}} is, who it's for, what it does, and what it doesn't. Each statement carries a label saying how settled it is, and cites the decision behind it.

## Current direction

The few bets the team is making right now. New ideas, research and requests get weighed against these, rather than added beside them. When a bet changes, strike it through and add the new one, so the change stays visible.

| Bet | How settled | What would change it |
|---|---|---|
| {{e.g. Families first: a parent and a child, together}} | Early hunch · {{HYP-ID}} | {{e.g. Testers don't invite their family}} |
| {{…}} | Working direction · {{HYP-ID}} | {{…}} |
| {{…}} | Agreed with NYLIM · {{ID}} | {{…}} |

Keep it to three to five bets. "How settled" is one of: early hunch, working direction, or agreed with NYLIM. An unagreed bet cites its hypothesis, so the evidence on it shows up in the [evidence view](../_generated/evidence.md). An agreed bet cites its decision.

## How to read the labels

| Label | Means | Decision status |
|---|---|---|
| **Decided** | Agreed and recorded | `accepted` |
| **Proposed** | Written up, waiting for sign-off | `proposed` |
| **Open** | A question still to answer | `open` |
| **Out** | Deliberately not doing | `parked` / `superseded` |
| **Hypothesis** | Someone's working idea, not agreed or proven | none, but cites its HYP |

## Sections

| Section | What it covers |
|---|---|
| [Proposition](proposition.md) | What {{Product}} is, and why someone would choose it |
| [Audience](audience.md) | Who it's for first |
| [Principles](principles.md) | The rules the product doesn't bend |
| [Capabilities](capabilities.md) | What it does, and what's in each milestone |
| [Journeys](journeys.md) | How the capabilities connect for a person |
| [Milestones](milestones.md) | Who each milestone is for, and what it needs |
| [Out of scope](out-of-scope.md) | What {{Product}} won't do, and why |

Every statement is one line, a label and an ID. A statement with a decision behind it cites the decision. A Hypothesis cites its [hypothesis](../hypotheses/README.md), such as `**Hypothesis** · HYP-04`, and never restates it. While drafting, a Hypothesis can be written out without an ID. The script lists those, so they get logged.

Open questions are the decisions with status `open` in [`../decisions/`](../decisions/README.md).

A Hypothesis is something nobody has proven yet, which makes the Hypothesis rows a list of what to test. What the evidence says about each one, and which to test next, is in the [evidence view](../_generated/evidence.md).

## Change log

Newest first. Each change bumps the version above.

| Date | Change | Decision |
|---|---|---|
| YYYY-MM-DD | First version | {{IDs it adds or cites}} |
