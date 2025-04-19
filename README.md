# weather-data-service

## Quick Start: Docker Development


### 1. Build the development image
```sh
docker build -t weather-data-service .
```

### 2. Run the API server (example)
```sh
docker run --rm -it -p 8080:8080 weather-data-service
```

### 3. Run tests
```sh
docker run --rm -it weather-data-service pytest
```

> Optionally, use `docker-compose` for multi-service development (API, Airflow, GCS emulator, etc).

---

## Airflow Data Pipeline

This project includes an automated data pipeline using Apache Airflow to periodically fetch and store weather data for multiple cities.

### Running Airflow Locally

1. **Install dependencies:**
   - Ensure `apache-airflow` is in `requirements.txt` (already included).
   - (Recommended) Use Docker Compose for isolated Airflow + API development. Example `docker-compose.yml` is provided or can be added.

2. **Set environment variables:**
   - Configure `.env` or export variables in your shell:
     - `CITIES=London,Paris,Berlin` (comma-separated list)
     - `AIRFLOW__CORE__FERNET_KEY` (see below)
     - Other required variables (see `.env.example`)

   **Generating a Fernet Key for Airflow:**
   To enable secure variable encryption, Airflow requires a Fernet key. Generate one with:
   ```sh
   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
   ```
   Copy the output and set it as `AIRFLOW__CORE__FERNET_KEY` in your `.env` file.

3. **Start Airflow (Local Development Workflow):**
   - If using Docker Compose:
     ```sh
     docker compose up airflow-init  # One-time DB init
     docker compose up airflow-webserver airflow-scheduler
     ```
   - Or, to run Airflow natively:
     ```sh
     export AIRFLOW_HOME=$(pwd)/airflow_home
     airflow db init
     airflow scheduler &
     airflow webserver
     ```

4. **Create an Airflow Admin User:**
   - After initializing the database, create an admin user (replace values as needed):
     ```sh
     airflow users create \
       --username admin \
       --firstname Admin \
       --lastname User \
       --role Admin \
       --email admin@example.com \
       --password admin
     ```
   - If using Docker Compose, run this inside the Airflow webserver container:
     ```sh
     docker compose exec airflow-webserver airflow users create \
       --username admin \
       --firstname Admin \
       --lastname User \
       --role Admin \
       --email admin@example.com \
       --password admin
     ```

5. **Access the Airflow UI:**
   - Open [http://localhost:8084](http://localhost:8084) (or the port set in `docker-compose.yml`).
   - Log in with the credentials you just created (default: `admin`/`admin`).

6. **Trigger the DAG:**
   - The DAG is named `weather_data_pipeline` and will run on the schedule defined in `dags/weather_data_pipeline.py` (default: every hour).
   - You can trigger runs manually from the Airflow UI or CLI.

### Customizing the Pipeline
- **Cities:** Set the `CITIES` env variable (comma-separated).
- **Schedule:** Set the `PIPELINE_SCHEDULE` environment variable (cron string, e.g. `0 * * * *`, or timedelta string, e.g. `hours=2`) in your `.env` or shell. If not set, defaults to every hour. You can also change `schedule_interval` in `dags/weather_data_pipeline.py`.
- **Storage:** The pipeline will use GCS or local JSON depending on your environment/config.

### Testing the Pipeline
- Unit tests for the DAG logic are provided in `tests/dags/test_weather_data_pipeline.py` (uses mocks for external calls).

### Deploying to Google Cloud Composer
- To deploy the pipeline to Composer, copy the contents of `/dags` to your Composer environment's DAGs folder and ensure all required dependencies are present in Composer's PyPI dependencies (see `requirements.txt`).

---

## Project Overview

(Documentation sections to be added: architecture, API, pipeline, etc.)