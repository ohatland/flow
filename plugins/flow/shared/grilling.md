# Grilling: putting decisions to the user

Interview the user until you reach a shared understanding. Map the decisions as a **design
tree**: every decision branches into the decisions that hang off it.

Work in **rounds**. The **frontier** is every decision whose prerequisites are settled: the
questions you can ask now without guessing at answers you have not heard. Ask the whole
frontier in one round, number each question and give your recommended answer. Then wait.

Ask in the user's language. Format:

```
**Q1 - <question title>**: <question body, with the options>

-> Recommended: <your recommended answer and why, briefly>

---

**Q2 - <question title>**: ...
```

Word each question so that "yes" accepts your recommended answer. The user can then
approve a whole round with "yes to all" without accidentally choosing the other option.

Each answered round reshapes the tree: recompute the frontier and ask the next round. A
question that depends on another question still open in this round goes in the same round
when your recommendation for the parent is firm: ask it under that assumption, marked
"if Q1 = a", so one round usually settles a step, and it lapses if the user chooses
otherwise. Only a child whose parent is a genuine toss-up waits for the next round.

Finding **facts** is your job, never the user's. When a question needs a fact from the code,
the docs or tools, ask the step's architect for it (`SendMessage`; `orchestrating.md`, "One
agent per role"), or an Explore agent when no architect is running; do not ask the
user for anything you could look up. Only the questions downstream of a running lookup wait.
The **decisions** are the user's.

Spend the user's attention on what they control: the contract categories in the profile
(`.flow/project.md`, `## Contract`) and recorded decisions such as ADRs. Decide internal code
structure yourself instead of asking.

Done when the frontier is empty and the user confirms the shared understanding.
