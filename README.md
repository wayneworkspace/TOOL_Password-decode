# Excel Password Decoder

![Python](https://img.shields.io/badge/python-3.13-blue)
![Security](https://img.shields.io/badge/security-msoffcrypto-success)

A high-performance, multi-core CLI tool to recover passwords and decrypt password-protected Microsoft Excel 97-2003 (`.xls`) workbooks using RC4 CryptoAPI verification and ProcessPoolExecutor parallel workers. Built with Python 3.13, msoffcrypto, olefile, and concurrent.futures.

## 1. Business Context & Goals

* **Business problem:** Legacy Microsoft Excel 97-2003 workbooks (`.xls`) containing critical business formulas and proprietary formulations (such as `Wet BI formulation.xls`) can be locked with lost or forgotten passwords. Traditional brute-force tools either corrupt workbook streams or decrypt the entire file per attempt (which drops throughput to <200 pwd/s).
* **Project goal:** Extract FilePass encryption parameters (salt and verifier) directly from the OLE stream, verify candidate passwords at 50,000+ pwd/s per core across all available CPU threads using `msoffcrypto`, and automatically decrypt the workbook to clean `.xls` once found.

## 2. Pipeline Architecture

```text
[Encrypted .xls] -> [OLE Workbook Stream] -> [FilePass Record (0x002F)]
                                                   │
                   ┌───────────────────────────────┴───────────────────────────────┐
                   ▼                                                               ▼
        [Phase 1: Wordlist Scan]                                      [Phase 2: Multi-core Brute-force]
        (Lines streamed in chunks)                                    (ProcessPoolExecutor Workers)
                   │                                                               │
                   └───────────────────────────────┬───────────────────────────────┘
                                                   ▼
                                     [msoffcrypto RC4 Verifier]
                                                   │
                                     [Match Found: Save to secrets/]
                                                   │
                                                   ▼
                                         [Decrypted Output .xls]
```

| Step | Description | Source code path |
| --- | --- | --- |
| **Configuration** | Runtime parameters, worker counts, charset, and file paths via immutable `Settings` dataclass | `src/config.py` |
| **Crypto & OLE Parser** | Stream reading, FilePass 0x002F record extraction, verifier validation, and final document decryption | `src/crypto.py` |
| **Cracker & Workers** | Parallel worker slicing, line-by-line wordlist scanner, and combinatoric candidate generator | `src/cracker.py` |
| **Execution** | Central CLI entry point orchestrating sanity checks, scanning phases, result logging, and decryption | `main.py` |
| **Automated Testing** | Pytest unit test suite covering parameter extraction, password validation, file decryption, and prefix search | `tests/` |

## 3. Technologies Used & Rationale

| Category | Technology | Rationale |
| --- | --- | --- |
| **Core Runtime** | Python 3.13 | Native generic unions (`str \| None`), PEP 695 syntax, high performance, and standard library optimizations |
| **Decryption Engine** | `msoffcrypto-tool` (`msoffcrypto`) | Official implementation for Microsoft Office encryption; verifies RC4 CryptoAPI passwords without rolling custom crypto |
| **Binary Parser** | `olefile`, `struct` | Safely navigates OLE2 compound document structures and streams without loading entire 700KB workbook into memory repeatedly |
| **Concurrency** | `concurrent.futures.ProcessPoolExecutor` | Eliminates Python Global Interpreter Lock (GIL) constraints with clean, idiomatic task distribution |
| **Code Quality** | Ruff, Pytest | Enforces strict PEP 8 formatting, import organization, and zero-defect linting with sub-second unit test validation |

## 4. Results Achieved

* **Recovery throughput:** Achieved ~51,500 verifications per second per CPU core (~800,000 pwd/s aggregate across 16 CPU cores), compared to standard full-file decryption throughput of ~172 pwd/s (a >4,500x speedup).
* **Target solved:** Successfully cracked and recovered the password (`12345`) for `Wet BI formulation.xls` from an exhaustive 26-million combination search space in ~32 seconds.
* **Storage & Lean:** Purged 614 MB of raw candidate dumps down to a lean, modular 3-file architecture under `src/` (<220 lines total across entire codebase).
* **Test coverage:** 100% pass rate across 6 automated unit tests in `0.30s`.

*(Current limitations: Specifically targets Microsoft Excel 97-2003 Binary File Format (BIFF8) with RC4 CryptoAPI encryption; does not target OOXML `.xlsx` agile encryption (ECMA-376) or legacy XOR obfuscation).*

## Quick Start

### Prerequisites

* [Python 3.13](https://www.python.org/) or [uv](https://docs.astral.sh/uv/)
* Dependencies: `msoffcrypto-tool`, `olefile`, `pytest`, `ruff`

### Install and run

```powershell
# 1. Clone the repository
git clone <repository-url>
cd Password_extract

# 2. Install dependencies
uv pip install -r requirements.txt   # or: pip install msoffcrypto-tool olefile pytest ruff

# 3. Configure environment variables (optional)
copy .env.example .env

# 4. Place target file in data/ and run password extraction
python main.py
```

## Project Structure

```text
data/           # Target encrypted files and unlocked output workbooks
secrets/        # Recovered credentials and sensitive password records (git-ignored)
src/            # Modular Python source code (config.py, crypto.py, cracker.py)
tests/          # Pytest automated unit tests
main.py         # Primary CLI orchestration entry point
.env.example    # Environment variable template
.gitignore      # Exclusion list for secrets, data, logs, and caches
```

> **Note:** Never commit `secrets/`, actual passwords, or proprietary customer `.xls` files in `data/`. Work on feature branches (`feature/...`, `fix/...`) and merge through Pull Requests passing all automated test suites.
