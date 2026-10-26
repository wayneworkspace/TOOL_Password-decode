---
trigger: model_decision
description: Apply when creating, moving, or deciding where to put files or folders, or when touching .gitignore, secrets, logs, or output
---

# Repository Directory Rules

## 1. Standard Directory Structure

```
unified_data_project/
│
├── .github/workflows/        # CI/CD pipelines (GitHub Actions)
│   ├── ci_test.yml           # On every Pull Request: dbt tests, Python tests, linting
│   └── cd_deploy.yml         # On merge to main: deploy DAGs, run dbt seed/run on Production
│
├── .gitignore                # Files/folders excluded from Git
├── .env.example              # Environment variable template (no real secrets)
├── README.md                 # Project overview and documentation
├── Dockerfile                # Custom image with Airflow, dbt, and required libraries
├── docker-compose.yaml       # Simulate the whole system locally for development
├── requirements.txt          # Required Python libraries
│
├── infra/                    # Infrastructure as code (DevOps)
│   ├── terraform/            # Provision Snowflake, S3, IAM roles, etc.
│   ├── k8s/                  # Kubernetes manifests (if running Airflow on K8s)
│   └── scripts/              # Deployment scripts (e.g., deploy.sh)
│
├── config/                   # Runtime configuration
│   └── airflow_local_settings.py  # Airflow colored logging config
│
├── secrets/                  # Real secret files such as .env (git-ignored)
│
├── output/                   # Dated code review reports (git-ignored)
│   └── DD-MM-YYYY.md         # One report per review run
│
├── logs/                     # All logs (git-ignored)
│   ├── airflow/              # Airflow's automatic task logs
│   ├── dbt/                  # dbt run logs
│   ├── custom_scripts/       # Logs from the Python code in src/
│   └── infra/                # Terraform, Kubernetes, and Docker logs
│
├── src/                      # Python source code, split by pipeline stage
│   ├── 1_source/
│   ├── 2_ingestion/
│   ├── 3_storage/
│   ├── 4_transform/
│   ├── 5_serving/
│   └── 0_utils/              # Shared helpers (e.g., logger.py)
│
├── dags/                     # Airflow DAG definitions
│   ├── main_etl_dag.py       # Main DAG orchestrating the whole pipeline
│   └── utils_dag.py          # Shared helper functions for DAGs
│
├── dbt_project/              # Entire dbt project (data transformation)
│   ├── dbt_project.yml       # Main dbt configuration
│   ├── profiles.yml          # Warehouse connection (Snowflake, BigQuery, etc.)
│   ├── models/               # Transformation models (SQL / Python models)
│   │   ├── staging/          # Raw data cleaning (stg_*.sql)
│   │   └── marts/            # Business-ready aggregates (dim_*, fact_*)
│   ├── tests/                # dbt data integrity tests
│   └── seeds/                # Static CSV data loaded into the warehouse
│
├── include/                  # Supporting files for DAGs
│   ├── sql/                  # Plain SQL statements (when not using dbt)
│   └── scripts/              # Auxiliary Python or Bash scripts
│
├── plugins/                  # Airflow custom Operators, Hooks, Sensors
│   └── custom_operators.py   # Company-specific custom logic
│
└── tests/                    # Unit tests (Python code and DAG validation)
    ├── test_dag_integrity.py # Checks DAGs for syntax/import errors
    └── test_custom_code.py   # Tests for custom Python functions
```

## 2. Folder Responsibilities

- `src/` holds importable production Python code split into five stages.
- `dags/` holds orchestration only, with minimal business logic inside.
- `dbt_project/` holds every SQL transformation plus its data quality tests.
- `include/` holds supporting SQL and scripts belonging to the DAGs.
- `plugins/` holds reusable Airflow Operators, Hooks, and custom Sensors.
- `infra/` holds Terraform and Kubernetes infrastructure code.
- `.github/workflows/` holds CI and CD definitions.
- `config/` holds runtime configuration such as Airflow logging settings.
- `secrets/` holds real secret files and must stay git-ignored.
- `output/` holds dated review reports; see REVIEW_RULES.md for format.
- `logs/` holds all log output and must stay git-ignored permanently.
- `src/0_utils/` holds shared helpers and is the only non-stage folder.
- `tests/` holds unit tests and Airflow DAG integrity validation.
- Never commit secrets or large datasets; exclude them via `.gitignore`.

## 3. No `__init__.py` Files

- Create no `__init__.py` file anywhere inside this entire repository.
- Rely on Python implicit namespace packages for resolving all imports.
- Configure `pytest` paths through `pyproject.toml`, not package marker files.
- Load digit-prefixed folders with `importlib.import_module` or by file path.
