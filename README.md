# 💤 Sleep Health Data Pipeline — Airflow + dbt + Cosmos + DuckDB

A complete **modern ELT pipeline** built with
**Apache Airflow**, **dbt**, **DuckDB**, and **Astronomer Cosmos**.
This project ingests, transforms, and validates the *Sleep Health and Lifestyle* dataset from Kaggle — all fully orchestrated in Airflow.

---

## 📘 Table of Contents

* [Overview](#-overview)
* [Architecture](#-architecture)
* [Tech Stack](#-tech-stack)
* [Project Structure](#-project-structure)
* [Setup Instructions (Windows)](#-setup-instructions-windows)
* [Running the Pipeline](#-running-the-pipeline)
* [SQL Model Description](#-sql-model-description)
* [How It Works](#-how-it-works)
* [Next Steps](#-next-steps)

---

## 🧠 Overview

This project demonstrates how to orchestrate **data transformations** using
**dbt** and **Airflow**, with **Cosmos** bridging the two.

#### Sleep Health and Lifestyle Dataset — Overview

The **Sleep Health and Lifestyle Dataset** contains anonymized information about individuals’ sleep patterns and lifestyle habits. It includes attributes such as **gender, occupation, sleep duration, sleep quality, stress level, BMI, physical activity, and heart rate**.

The dataset is commonly used for **analyzing the relationship between lifestyle factors and sleep quality**, helping uncover insights like how occupation, stress, or physical activity influence overall sleep health.

* **Records:** 374 individuals
* **Key Features:** Sleep Duration, Quality of Sleep, Stress Level, Physical Activity Level, Age, Occupation, BMI, Gender, Heart Rate, Daily Steps
* **Source:** [Kaggle – Sleep Health and Lifestyle Dataset](https://www.kaggle.com/datasets/uom190346a/sleep-health-and-lifestyle-dataset)

#### Pipeline Summary:

1. Load the *Sleep Health and Lifestyle* CSV dataset into DuckDB
2. Run dbt models to clean, aggregate, and analyze the data
3. Validate results using dbt tests
4. Orchestrate and automate the entire flow using Airflow DAGs

---

## 🏗️ Architecture

```text
             ┌───────────────────────────────────────────┐
             │               Apache Airflow              │
             │         (pipeline orchestration)          │
             └───────────────┬───────────────────────────┘
                             │
                   DbtTaskGroup (Cosmos)
                             │
         ┌───────────────────┴────────────────────┐
         │                                        │
     dbt seed/run/test                     Custom Airflow Tasks
 (Transformations in SQL)                (e.g., load_csv_to_duckdb)
         │                                        │
         └───────────────────┬────────────────────┘
                             │
                      🦆 DuckDB Database
                  (storage + query execution)
```

---

## ⚙️ Tech Stack

| Component                  | Purpose                                |
| -------------------------- | -------------------------------------- |
| **Apache Airflow**         | Workflow orchestration and automation  |
| **dbt (Data Build Tool)**  | SQL-based data transformations         |
| **Cosmos (by Astronomer)** | Integrates dbt projects into Airflow   |
| **DuckDB**                 | Lightweight analytical database engine |
| **Astronomer CLI (Astro)** | Local Airflow environment setup        |
| **Python 3.12+**           | Core runtime                           |

---

## 📁 Project Structure

```text
sleep-health-data-pipeline/
├── dags/
│   ├── sleep_health_full_pipeline.py     # Main Airflow DAG
│   └── dbt/
│       └── sleep_health_lifestyle/
│           ├── dbt_project.yml           # dbt project configuration
│           ├── models/
│           │   ├── sleep_analysis/
│           │   │   ├── sleep_summary.sql
│           │   │   ├── occupation_stresslevels.sql
│           │   │   ├── occupation_gender.sql
│           │   │   ├── dailysteps_bmi.sql
│           │   │   ├── sources.yml
│           │   │   └── schema.yml
│           └── target/                   # dbt compiled outputs
│
├── include/
│   ├── sleep_health.csv                  # raw dataset
│
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🪜 Setup Instructions (Windows)

### 1. Clone or Download the Repository

### 2. Install Prerequisites

* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* [Astronomer CLI](https://www.astronomer.io/docs/astro/cli/install-cli)
* [Python 3.12+](https://www.python.org/downloads/)
* [Git](https://git-scm.com/)


### 3. Initialize and Start Airflow
```bash
astro dev init
```

```bash
astro dev start
```

Once running:

* Airflow UI → [http://localhost:8080](http://localhost:8080)

---

## 🚀 Running the Pipeline

In the Airflow UI:

1. Enable the DAG: **`sleep_health_full_pipeline`**
2. Trigger it manually (▶️ Run)

The DAG will:

1. Load your CSV into DuckDB (`load_csv_to_duckdb`)
2. Run all dbt models sequentially (`DbtTaskGroup`)
3. Validate data quality (dbt tests)
4. Generate transformed tables like `sleep_summary`, `occupation_stresslevels` etc.

---

## 🧩 SQL Model Description

| **Model**                   | **File Path**                                       | **Description**                                                                                                                                        |
| --------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **sleep_summary**           | `models/sleep_analysis/sleep_summary.sql`           | Aggregates average sleep duration, quality, stress, and physical activity across all participants to provide an overall view of sleep health patterns. |
| **occupation_gender**       | `models/sleep_analysis/occupation_gender.sql`       | Compares sleep duration and quality across different occupations segmented by gender, identifying potential lifestyle-based differences.               |
| **dailysteps_bmi**          | `models/sleep_analysis/dailysteps_bmi.sql`          | Examines the relationship between participants’ daily steps and their BMI to identify how physical activity correlates with body mass index.           |
| **occupation_stresslevels** | `models/sleep_analysis/occupation_stresslevels.sql` | Calculates average stress levels grouped by occupation to pinpoint job categories associated with higher stress and poorer sleep quality.              |

Each model becomes a view or table in DuckDB once dbt runs.

---

## 🔍 How It Works

| Step | Component               | Description                                      |
| ---- | ----------------------- | ------------------------------------------------ |
| 1    | **Airflow**             | Orchestrates workflow scheduling                 |
| 2    | **Custom Python Task**  | Loads CSV → DuckDB                               |
| 3    | **Cosmos DbtTaskGroup** | Runs dbt models + tests                          |
| 4    | **dbt**                 | Executes SQL transformations                     |
| 5    | **DuckDB**              | Stores transformed results                       |
| 6    | **Airflow DAG**         | Ensures proper task ordering (`load_csv >> dbt`) |

---

## 💻 Common Commands

| Command             | Description                              |
| ------------------- | ---------------------------------------- |
| `astro dev start`   | Start local Airflow environment          |
| `astro dev restart` | Rebuild containers and reload DAGs       |
| `astro dev stop`    | Stop Airflow environment                 |
| `astro dev bash`    | Enter Airflow container                  |

---

## 🧮 Example Output

1. Open your favourite IDE.

2. If DuckDB is not already installed:
   ```python
   pip install duckdb
   ```

3. Create a ```test.py``` in the same directory as the project folder.

4. Run an example query:
   ```python
   import duckdb

   con = duckdb.connect("sleep-health-data-pipeline/include/sleep_health_lifestyle.duckdb")
   con.sql("SELECT * FROM sleep_summary LIMIT 10").show()
   con.close()
   ```

✅ You’ll see aggregated sleep metrics by occupation.

---

## 🌙 Next Steps

* Add **dbt tests** (e.g., check that Sleep Duration > 0)
* Schedule DAGs to run daily or hourly
* Visualize results in **Metabase** or **Superset**
* Migrate from DuckDB → Postgres / Snowflake for scalability
* Deploy to **Astronomer Cloud** for production orchestration
