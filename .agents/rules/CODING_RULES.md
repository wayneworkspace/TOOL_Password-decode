---
trigger: always_on
description: Behavioral coding rules: think first, simplicity, surgical changes, goal-driven execution
---

# Coding Behavior Rules

Behavioral rules that reduce common LLM coding mistakes across projects.

**Tradeoff:** These rules favor caution over speed; use judgment on trivial tasks.

## 1. Think Before Coding

**Do not assume, do not hide confusion, always surface tradeoffs.**

- State assumptions explicitly before coding; ask when requirements stay unclear.
- Present every plausible interpretation openly; never pick one silently.
- Propose the simpler approach directly and push back when warranted.
- Stop when confused, name the exact blocker, then ask.

## 2. Simplicity First

**Write minimum code that solves the problem, nothing speculative.**

- Build no features beyond the exact scope the user requested.
- Implement the requested functionality only, never hypothetical future situations.
- Write no code path for scenarios that do not exist.
- Avoid abstractions and wrappers for code used only once.
- Add no flexibility or configurability that nobody ever requested.
- Skip error handling for scenarios that physically cannot occur.
- Rewrite any 200-line solution that fits in 50 lines.
- Ask whether a senior engineer would call this overcomplicated.

## 3. Surgical Changes

**Touch only what you must, clean up only your mess.**

- Never improve adjacent code, comments, or formatting without being asked.
- Refactor nothing that currently works and is not broken.
- Match the existing code style even when you would differ.
- Mention unrelated dead code to the user, but never delete it.
- Remove imports, variables, functions that your own changes made unused.
- Leave pre-existing dead code untouched unless explicitly asked otherwise.
- Every changed line must trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria first, then loop until fully verified.**

Transform vague tasks into verifiable goals:

- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure the full test suite passes before and after"

For multi-step tasks, state a brief plan before starting:

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

- Strong success criteria enable independent looping without constant clarification.
- Weak criteria such as "make it work" stall progress repeatedly.

## 5. Library Over Built-in

**Reach for a tested library before writing primitive code.**

- Reach for an importable library before any Python built-in function.
- Use built-ins only when no suitable library covers the need.
- Prefer stdlib modules such as `itertools` over manual built-in loops.
- Keep the order fixed: library first, built-in second, manual loop last.
- Justify every new dependency this rule introduces before adding it.
- Never hand-roll logic that a well-tested library already solves.

---

**These rules work when:** diffs contain fewer unnecessary changes, overcomplication causes fewer rewrites, and clarifying questions arrive before implementation rather than after mistakes.
