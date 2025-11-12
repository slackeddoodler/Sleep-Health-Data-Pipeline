from airflow.decorators import task
from airflow import DAG
from cosmos import DbtTaskGroup
import duckdb
from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles.duckdb import DuckDBUserPasswordProfileMapping
from pendulum import datetime
import os
from pathlib import Path

@task
def load_csv_to_duckdb():
    db_path = "/usr/local/airflow/include/sleep_health_lifestyle.duckdb"
    csv_path = "/usr/local/airflow/include/sleep_health_and_lifestyle_dataset.csv"
    con = duckdb.connect(db_path)
    con.execute(f"""
        CREATE TABLE IF NOT EXISTS sleep_health AS
        SELECT * FROM read_csv('{csv_path}');
    """)
    con.close()

DUCKDB_CONN_ID = os.getenv("DUCKDB_CONN_ID", "duckdb_default")
DBT_PROJECT_NAME = "sleep_health_lifestyle"
DBT_PROJECT_PATH = (Path(__file__).parent / "dbt" / DBT_PROJECT_NAME).resolve().as_posix()
DBT_EXECUTABLE_PATH = f"{os.getenv('AIRFLOW_HOME')}/dbt_venv_duckdb/bin/dbt"

_project_config = ProjectConfig(dbt_project_path=DBT_PROJECT_PATH)
_profile_config = ProfileConfig(
    profile_name="default",
    target_name="dev",
    profile_mapping=DuckDBUserPasswordProfileMapping(
        conn_id=DUCKDB_CONN_ID,
        profile_args={"path": "/usr/local/airflow/include/sleep_health_lifestyle.duckdb", "schema": "main"},
    ),
)
_execution_config = ExecutionConfig(dbt_executable_path=DBT_EXECUTABLE_PATH)

with DAG(
    dag_id="sleep_health_full_pipeline",
    catchup=False,
    max_active_tasks=1
) as dag:

    load_csv = load_csv_to_duckdb()
    dbt_tg = DbtTaskGroup(
        group_id="sleep_health_dbt",
        project_config=_project_config,
        profile_config=_profile_config,
        execution_config=_execution_config,
    )
    load_csv >> dbt_tg