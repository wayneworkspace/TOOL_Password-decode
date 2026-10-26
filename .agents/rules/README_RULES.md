---
trigger: glob
description: Required README sections, writing rules, and template
globs: "**/README.md"
---

# README Rules

A README is the first thing a reader sees. It must explain the problem, the architecture, the technologies, and the results, and let anyone run the project quickly.

---

## 1. Required Sections

Every README must contain these sections, in this order:

| # | Section | Purpose |
|---|---------|---------|
| – | **Title, badges, short description** | Project name, CI / Python / Cloud badges, and a 1-2 sentence summary: what the project does, what problem it solves, and the core technologies. |
| 1 | **Business Context & Goals** | The real business problem, and what the project builds to solve it. |
| 2 | **Pipeline Architecture** | A diagram of the data flow plus a table describing each step and where its code lives. |
| 3 | **Technologies Used & Rationale** | Each technology and *why* it was chosen. |
| 4 | **Results Achieved** | Measurable outcomes: data volume, performance, cost, insights delivered. Also current limitations. |
| – | **Quick Start** | Prerequisites and copy-paste steps to install and run the project (locally and with Docker). |
| – | **Code Quality & CI/CD** | Commands to run before a Pull Request, and a summary of the CI and CD pipelines. |
| – | **Project Structure** | Short map of the main folders. |
| – | **Note** | Security warnings and conventions (secrets, branch naming, etc.). |

---

## 2. Writing Rules

- Replace every placeholder; leave no `[...]` text in finished READMEs.
- Keep real command arguments such as `<repository-url>` exactly as written.
- Use real numbers in Results, never vague unmeasurable marketing claims.
- Give every technology row a concrete rationale, not just its name.
- Map each pipeline step to the folder containing its source code.
- State limitations honestly: local-only, pre-production, or service-account usage.
- Make Quick Start commands copy-pasteable and tested on clean machines.
- Never include keys, passwords, or real credentials anywhere in documentation.
- Reference `.env.example` and tell readers to keep `secrets/` ungitted.
- Update the README inside the same Pull Request as the change.
- Keep badges accurate: real workflow file and the actual Python version.
- Write the entire README in English for every reader.

---

## 3. README Template

Copy this template into `README.md` and fill it in.

````markdown
# [Project Name]

[![CI](https://github.com/username/repo/actions/workflows/ci_test.yml/badge.svg)](https://github.com/username/repo/actions/workflows/ci_test.yml)
![Python](https://img.shields.io/badge/python-3.13-blue)
![Cloud](https://img.shields.io/badge/cloud-GCP/AWS-4285F4)

[1-2 sentence summary: what the project does, what problem it solves, and the core technologies it uses.]

## 1. Business Context & Goals

* **Business problem:** [Describe the real difficulty or problem the business or system is facing.]
* **Project goal:** [What system is built, and what specific result it achieves to solve the problem above.]

## 2. Pipeline Architecture

```text
[Data sources] -> [Ingestion / Raw] -> [Bronze] -> [Silver] -> [Gold] -> [Serving / BI]
```

| Step | Description | Source code path |
| --- | --- | --- |
| **Ingestion** | [Fetch data from sources into raw storage...] | `src/2_ingestion/` |
| **Bronze** | [Load raw data into the data warehouse...] | `src/3_storage/` |
| **Silver** | [Clean, standardize data types, build facts/dims...] | `dbt_project/models/staging/` |
| **Gold** | [Apply business rules, aggregate for reporting...] | `dbt_project/models/marts/` |
| **Serving** | [Serve data to dashboards / APIs / apps...] | `src/5_serving/` |

## 3. Technologies Used & Rationale

| Category | Technology | Rationale |
| --- | --- | --- |
| **Cloud / Warehouse** | [Google Cloud Storage, BigQuery] | [Handles large data, integrates well with dbt, cost-efficient...] |
| **Transformation** | [dbt (dbt-bigquery)] | [Modular SQL, built-in testing and lineage graph...] |
| **Orchestration** | [Apache Airflow] | [Schedules complex tasks, clear dependency tracking...] |
| **Code & Quality** | [Python, Ruff, Mypy, SQLFluff] | [Keeps code clean and catches errors before production...] |

## 4. Results Achieved

* **Data volume:** [Example: processes X million records per day / Y GB.]
* **Performance / Optimization:** [Example: pipeline runtime reduced to Z minutes, storage cost reduced...]
* **Insights / Value delivered:** [Example: real-time reports that support business decisions.]

*(Current notes / Limitations: Example - not yet running in production, runs locally with a service account, etc.)*

## Quick Start

### Prerequisites

* [Tool 1, e.g., uv / pip]
* [Tool 2, e.g., Docker & Docker Compose]
* [Cloud account / secrets configuration file]

### Install and run

```powershell
# 1. Clone the repository
git clone <repository-url>
cd <repository-name>

# 2. Install the environment and dependencies
uv sync

# 3. Configure environment variables
copy .env.example secrets/.env   # Fill in your own configuration

# 4. Run the pipeline / initialize the system
uv run python <path-to-entrypoint>
```

Run with Docker (if available):

```powershell
docker compose --env-file secrets/.env up -d --build
```

## Code Quality & CI/CD

Before opening a Pull Request, make sure all of these checks pass:

```powershell
uv run ruff check .
uv run ruff format --check .
uv run mypy
```

* **CI pipeline:** runs pre-commit, linters, and dbt parse automatically on GitHub Actions.
* **CD pipeline:** builds and pushes the image automatically when code is merged into `main`.

## Project Structure

```text
src/                # Main source code (source, ingestion, storage, transform, serving)
dags/               # Airflow DAGs
dbt_project/        # dbt project (models, seeds, tests)
infra/              # Terraform, Kubernetes, deployment scripts
```

> **Note:** [Security notes: never commit the `secrets/` folder or any keys, branch naming conventions, etc.]
````
