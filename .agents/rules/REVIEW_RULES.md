---
trigger: manual
description: Code review pass with Jev: optimization, vulnerabilities, expansion advice, dated report
---

# Code Review Rules (Jev)

Rules for the review pass that optimizes code, finds vulnerabilities, advises expansion, and writes one dated report.

---

## 1. Setup

- Add `typesafe-sdk` to the `dev` extra; the pipeline image never calls Jev.

## 2. API Key Handling

- Store the Jev key as `TYPESAFE_API_KEY` inside `secrets/.env`.
- Never commit `secrets/.env`; list the whole folder in `.gitignore`.
- List `TYPESAFE_API_KEY` in `.env.example` with a placeholder value.
- Read the key through `os.environ`, never hard-coded in source.
- Keep the key server-side and out of every frontend bundle.
- Never print the key into logs or the generated report.

## 3. Division of Labour

- Jev returns typed judgments only, never prose or explanations.
- The agent performs the analysis and writes the entire report text.
- Send Jev `Choice`, `Score`, and `Noul` questions over one state.
- Ask independent questions together so they run fully in parallel.
- Escalate back to the agent whenever Jev returns `escalate: true`.

## 4. Code Optimization

- Apply `CODING_RULES.md` (Simplicity First, Surgical Changes) to each proposed fix.
- Ask Jev to score each optimization by its real impact.
- Propose deletion before abstraction whenever both solve the problem.
- Reject any suggestion adding dependencies without clear written justification.
- Quote the exact file and line beside every proposed change.

## 5. Vulnerability Findings

- Scan for injection, secret leaks, and missing input validation.
- Check authentication, authorization, and unsafe deserialization in every service.
- Ask Jev one `Noul` question per finding about real exploitability.
- Ask Jev one `Score` question to rank each finding's severity.
- Drop findings whose exploitability probability falls below the 0.5 threshold.
- Never claim a vulnerability without naming its exact file path.
- Treat this review as no substitute for a real security review.
- Report the vulnerability class, never a working exploit payload.

## 6. Expansion Advice

- Base every expansion suggestion on the five existing pipeline stages.
- Ask Jev to rank proposed expansions by estimated business value.
- State the cost and the risk beside each expansion suggestion.
- Suggest no expansion that breaks the stage dependency direction.
- Mark advice as speculative when no production data supports it.

## 7. Report Output

- Write one report per review run into the `output/` folder.
- Name the file `DD-MM-YYYY.md` from the current local date.
- Use hyphens, because slashes are illegal inside every filename.
- Overwrite the same-day report instead of creating numbered duplicate files.
- Git-ignore `output/` because reports name unpatched live vulnerabilities.
- Include all three sections even when one section finds nothing.
- Write every report in English, following the template below.

### Report Template

````markdown
# Code Review Report — [DD-MM-YYYY]

* **Commit reviewed:** [short SHA]
* **Scope:** [folders or files reviewed]
* **Jev judgments requested:** [count]

## 1. Optimization

| File:Line | Current | Proposed | Jev impact score |
| --- | --- | --- | --- |
| [`src/2_ingestion/load.py:42`] | [What the code does now] | [Minimal replacement] | [0.0-1.0] |

## 2. Vulnerabilities

| File:Line | Class | Jev exploitability | Jev severity | Fix |
| --- | --- | --- | --- | --- |
| [`src/5_serving/api.py:17`] | [SQL injection] | [0.0-1.0] | [0.0-1.0] | [Minimal fix] |

*(Findings below the 0.5 exploitability threshold were dropped: [count].)*

## 3. Expansion Advice

| Suggestion | Stage | Jev value rank | Cost | Risk |
| --- | --- | --- | --- | --- |
| [What to build] | [`3_storage`] | [0.0-1.0] | [Effort] | [What could break] |

## Escalations

* [Questions Jev returned with `escalate: true`, and the agent's own judgment.]
````
