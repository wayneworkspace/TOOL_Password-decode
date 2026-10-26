---
trigger: glob
description: Python 3.13 style and data-processing rules
globs: "**/*.py"
---

# Python Rules

Target **Python 3.13** and keep every module minimal.

## 1. Data Processing and Robustness

**Required topics:** `pandas`, file processing, API calls, retry logic, logging.

- Use pandas vectorized operations instead of slow row-by-row loops.
- Handle encoding, missing files, and malformed rows in every reader.
- Read large files in chunks instead of loading everything at once.
- Give every API call timeouts, error handling, and exponential-backoff retries.
- Use the `logging` module with enough context to debug failures.
- Never call `print()` for runtime messages anywhere in production code.

## 2. Code Style

- Write the least code that clearly does the required job.
- Ship no dead code, unused abstractions, or redundant restating comments.
- Use built-in generics and union syntax: `list[str]`, `dict[str, int]`, `str | None`.
- Never import `List`, `Dict`, `Optional`, or `Union` from `typing`.
- Declare type aliases with the `type` statement, not `TypeAlias`.
- Write generics using PEP 695 syntax instead of `TypeVar`.
- Prefer `pathlib` over `os.path`, and f-strings over `.format()`.
- Use `dataclass` with `slots=True` and `frozen=True` where suitable.
- Use `match` statements where they beat long `if/elif` chains.
- Open files, connections, and sessions through context managers only.
- Prefer libraries first, then built-ins, then manual loops last.
- Use comprehensions where they read better than an explicit loop.
- Use the walrus operator only when it genuinely improves readability.
- Never add `from __future__ import annotations`; Python 3.13 makes it unnecessary.
- Create no `__init__.py` files anywhere; see DIRECTORY_RULES.md for details.
- Format and lint with `ruff`; keep every function single-purpose.

Example:

```python
import logging
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

log = logging.getLogger(__name__)

type Row = dict[str, object]


@dataclass(frozen=True, slots=True)
class Source:
    name: str
    path: Path


def load(source: Source) -> pd.DataFrame:
    log.info("Loading %s from %s", source.name, source.path)
    return pd.read_csv(source.path)
```
