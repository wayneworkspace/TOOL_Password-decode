---
trigger: always_on
description: Index of all repository rules, precedence and reading order
---

# Rules Index

Entry point for this repository's rules. Antigravity loads this file on every turn (`trigger: always_on`), so every rule set below applies to all work here. All rule files live in `.agents/rules/`.

---

## Rule Files

| File | Trigger | Scope |
|------|---------|-------|
| `CODING_RULES.md` | always_on | Think before coding, simplicity, surgical changes, goal-driven execution |
| `DIRECTORY_RULES.md` | model_decision | Standard folder layout and the no-`__init__.py` rule |
| `PYTHON_RULES.md` | glob `**/*.py` | Python 3.13 style, pandas, retries, file handling |
| `GIT_RULES.md` | model_decision | Commit messages, feature branches, pull request flow |
| `README_RULES.md` | glob `**/README.md` | Required README sections, writing rules, and template |
| `REVIEW_RULES.md` | manual (`@REVIEW_RULES`) | Jev-assisted review, plus the dated report |

---

## Reading Order

- Read `CODING_RULES.md` before writing or editing any code.
- Read `DIRECTORY_RULES.md` before adding any files.
- Read the rule file matching your current technology before implementing.
- Read `REVIEW_RULES.md` before any optimization or vulnerability review pass.

## Precedence

- A rule file beats this index whenever the two ever disagree.
- An explicit user instruction beats every rule file in scope.
- Ask when two rule files genuinely conflict; never guess silently.
