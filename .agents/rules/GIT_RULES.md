---
trigger: model_decision
description: Apply when committing, naming branches, merging, or opening a pull request
---

# Git Rules

Use Git as real version control, not a file backup.

- Write imperative, descriptive commit messages following the Conventional Commits convention.
- Prefix commits correctly with `feat:`, `fix:`, `docs:`, or `refactor:`.
- Work on feature branches named like `feature/add-airflow-dag` or `fix/null-handling`.
- Merge every branch through a pull request, never directly into `main`.
- Make small, focused commits that show how the project evolved.
