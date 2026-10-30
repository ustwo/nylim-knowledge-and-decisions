# Scales and how the evidence is worked out

Every score in these docs uses one of three five-point scales. This page defines them, so a score means the same thing whoever sets it, a person or an AI. It also says what the script works out from them, so nobody has to.

The rule of thumb: **judge at the edges, compute the rest.** People judge three things: how much to trust a finding, how much an objective matters, and how strongly someone holds a hypothesis. Everything else is computed by [`scripts/evidence.py`](../scripts/evidence.py) and written to [`_generated/`](_generated/README.md). Computed values never go back into the source files.

## Trust: how far we can rely on a finding

Set on every finding. The AI suggests it, and a person checks it.

| Trust | Means | For example |
|---|---|---|
| **1** | Someone said it, and we can't check it. This includes a client's say-so | A client tells us advisers find the site slow |
| **2** | One source, with a method we can see. This includes a single interview, or a small study of ours | A published survey of 400 advisers, with its method stated |
| **3** | A consistent pattern across independent sources, or across the participants in a well-run study of ours | In concept testing, advisers consistently started with search |
| **4** | Underlying data we can check ourselves, and enough of it to rely on | Analytics from a beta with a few thousand users |
| **5** | System-of-record data at scale | A year of the client's own sales data |

- **Independent** means not drawing on the same original. Two articles quoting the same report are one source.
- **Trust is about the evidence, not how precise the claim sounds.** "Adoption is climbing" and "adoption is at 53%" can both be a 2. The claim's own wording says how definite it is.
- **Speculation isn't a finding.** A belief about what matters or what will work, ours or the client's, is a [hypothesis](hypotheses/README.md). A client telling us what *is* happening is a finding at trust 1.

## Starting confidence: how strongly a hypothesis is held

Set on every hypothesis, by or for whoever holds it. It records where we began, and it stays put while the evidence comes in. Change it only when the holder genuinely changes their mind, and say so in the file.

| Starting confidence | Means |
|---|---|
| **1** | A passing thought |
| **2** | Leaning towards it |
| **3** | Believe it, but could be persuaded |
| **4** | Confident |
| **5** | Treated as settled |

## Impact: the cost of being wrong

On hypotheses and decisions. It's usually computed, so most files never set it.

| Impact | Means |
|---|---|
| **1** | Trivial. Noticed and fixed in passing |
| **2** | Rework within a sprint |
| **3** | Rework across a milestone, or a visible miss on a secondary objective |
| **4** | A primary objective missed, or a costly change to undo |
| **5** | The engagement's core outcome at risk, or effectively irreversible |

**Where impact comes from:**

1. **From what it moves.** An item tagged with an objective or KPI takes its impact from that objective's rank in [`success.md`](success.md): north star 5, primary 4, secondary 3, tertiary 2.
2. **From what rests on it.** Impact flows upstream. A hypothesis that an impact-5 decision depends on is impact 5 too. A finding is as important as the most important thing it's evidence for.
3. **Set by hand,** with `impact` and an `impact_reason`, when reversibility changes the picture. The higher of the hand-set and computed values wins.
4. **Otherwise it's unknown,** and the script treats it as 3.

A decision at impact 4 or 5 is hard to undo, so it needs Drivers, Alternatives and Consequences (see [depth follows the stakes](README.md#depth-follows-the-stakes)). The script checks for them.

## What the script works out

### The evidence on a hypothesis or decision

Two values, from the findings linked to it.

**Strength (0 to 5): how much evidence there is.** Each finding adds weight by its trust:

| Trust | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Weight | 0.5 | 1 | 2 | 3 | 4 |

Findings that share a first source count once: the strongest of them. A `mixed` finding adds half its weight to each side. Strength is the total, capped at 5.

**Verdict: which way the evidence points.**

| Verdict | When |
|---|---|
| Untested | No linked findings |
| Supported | 70% or more of the weight supports it |
| Contested | Between 30% and 70% |
| Contradicted | 70% or more of the weight contradicts it |

Only reviewed, active findings count. Archived findings and unreviewed AI drafts don't.

### Confidence flows down, impact flows up

> source → finding → hypothesis → decision → KPI → objective

- **Impact flows upstream:** see above.
- **Contradictions flow downstream.** When the evidence moves against something, everything that depends on it is flagged too: "These decisions rest on something the evidence has moved against."

### The three lists

Written to [`_generated/evidence.md`](_generated/evidence.md):

| List | What's on it | Ranked by |
|---|---|---|
| **Needs a response** | Hypotheses and decisions the evidence has moved against, and what rests on them | Impact × contradicting weight |
| **Test next** | Hypotheses with little evidence either way | Impact × (5 − strength) |
| **Build on** | Hypotheses that are supported and well evidenced | Impact × strength |

When a hypothesis's starting confidence is 4 or more and the evidence contradicts it, it's flagged: "Starting confidence 4, but the evidence has moved."

### Seeds

A finding is a **seed** when nothing links it to a decision, hypothesis, KPI or objective. It's the same record with the same ID. "Seed" is only what we call it until something links to it. See [findings](findings/README.md#seeds).

All the thresholds and weights live in [`scripts/config.yaml`](../scripts/config.yaml). Change them there, and say why in the commit.
