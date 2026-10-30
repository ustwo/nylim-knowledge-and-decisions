# Decisions

Every decision that shapes {{Product}}, with the reasons for it. Each is one file in the folder for its kind, and its ID's prefix says who makes the call. The PRD, the architecture overview, build plans, code and commits cite them by ID, such as DES-07. An open question is a decision with status `open`.

**To add one:** copy [`_template.md`](_template.md) into the folder for its kind, give it the next number for its prefix, and set its status. When it replaces an earlier decision, list that one in `supersedes` and add the new ID to the earlier one's `superseded_by`. Then add its row below. The rules are in [How these docs work](../README.md#decisions).

The decisions below are starter questions most projects need answered early. Keep the ones that apply, and delete the rest.

## Product (PRD)

Product's calls: what {{Product}} does and for whom.

| ID | Question | Status | Date |
|---|---|---|---|
| [PRD-01](product/PRD-01.md) | Who is {{Product}} for first? | open | |
| [PRD-02](product/PRD-02.md) | Which journeys matter most in the first release? | open | |
| [PRD-03](product/PRD-03.md) | Where sources disagree, which one sets the baseline? | open | |
| [PRD-04](product/PRD-04.md) | What does the first milestone have to show, and to whom? | open | |
| [PRD-05](product/PRD-05.md) | Which KPIs show progress on each objective? | open | |

## Design (DES)

Design's calls: how {{Product}} works, looks and feels.

| ID | Question | Status | Date |
|---|---|---|---|
| [DES-01](design/DES-01.md) | Which platforms and screen sizes does {{Product}} support? | open | |
| [DES-02](design/DES-02.md) | If there's a design system, where do its values come from, and who changes them? | open | |
| [DES-03](design/DES-03.md) | What should {{Product}} feel like? | open | |

## Tech (TECH)

Tech's calls: how {{Product}} is built and run.

| ID | Question | Status | Date |
|---|---|---|---|
| [TECH-01](tech/TECH-01.md) | What is {{Product}} built with, and where does it run? | open | |
| [TECH-02](tech/TECH-02.md) | Where does the code live, and who owns it after handover? | open | |
| [TECH-03](tech/TECH-03.md) | How do we know a piece of work is done? | open | |

## Business (BIZ)

The business's calls: who {{Product}} serves and how it works as a business.

| ID | Question | Status | Date |
|---|---|---|---|
| [BIZ-01](business/BIZ-01.md) | Which objectives is {{Product}} measured against? | open | |
| [BIZ-02](business/BIZ-02.md) | How does {{Product}} make money? | open | |
