# weather-data-service

## Quick Start: Docker Compose (Recommended)

This is the easiest way to run the API server, Airflow, and other potential services together locally.

1.  **Configure Environment:**
    *   Copy `.env.example` to `.env`: `cp .env.example .env`
    *   Edit `.env` and set required variables (like `API_KEY`, `CITIES`, and generate `AIRFLOW__CORE__FERNET_KEY` - see Airflow section below).

2.  **Build and Start Services:**
    ```sh
    docker compose up --build -d
    ```
    *   This builds the images (if needed) and starts the API server (port 8080) and Airflow services (webserver on port 8084) in the background.
    *   Use `docker compose logs -f` to view logs.
    *   Use `docker compose down` to stop services.

3.  **Run Tests:**
    ```sh
    docker compose run --rm api pytest
    ```
    *   This runs the tests within a temporary container based on the `api` service definition in `docker-compose.yml`.

### Alternative: Individual Docker Commands

These commands are useful for running only the API service or specific tasks without Docker Compose.

*   **Build Image:**
    ```sh
    docker build -t weather-data-service .
    ```
*   **Run API Server Only:**
    ```sh
    # Ensure you have an API_KEY set in your environment or pass it via -e
    docker run --rm -it -p 8080:8080 -e API_KEY=$API_KEY weather-data-service
    ```
*   **Run Tests Only:**
    ```sh
    docker run --rm -it weather-data-service pytest
    ```

---

## Airflow Data Pipeline

This project includes an automated data pipeline using Apache Airflow to periodically fetch and store weather data for multiple cities.

### Running Airflow Locally (Docker Compose Recommended)

The recommended way to run Airflow locally is using Docker Compose, as described in the "Quick Start" section. This handles the setup of the scheduler, webserver, and database initialization.

1.  **Ensure `.env` is configured:** Make sure you have copied `.env.example` to `.env` and set the necessary variables, especially `CITIES` and `AIRFLOW__CORE__FERNET_KEY`.

    *   **Generating a Fernet Key:** If you haven't already, generate one:
        ```sh
        python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
        ```
        Copy the output and set it as `AIRFLOW__CORE__FERNET_KEY` in your `.env` file.

2.  **Start Services:**
    ```sh
    docker compose up --build -d
    ```
    *   This command (re-run if needed) starts the Airflow webserver, scheduler, and performs the initial database setup (`airflow-init` service runs once).

3.  **Create an Airflow Admin User (One-time setup):**
    *   After the services are running, execute the user creation command inside the webserver container:
        ```sh
        docker compose exec airflow-webserver airflow users create \
          --username admin \
          --firstname Admin \
          --lastname User \
          --role Admin \
          --email admin@example.com \
          --password admin
        ```
    *   *(Note: The `airflow-init` service in `docker-compose.yml` might handle initial user creation depending on its configuration)*

4.  **Access the Airflow UI:**
    *   Open [http://localhost:8084](http://localhost:8084) (or the port set in `docker-compose.yml`).
    *   Log in with the credentials you created (default: `admin`/`admin`).

5.  **Trigger the DAG:**
    *   The DAG is named `weather_data_pipeline` and will run on the schedule defined in `dags/weather_data_pipeline.py` (default: every hour).
    *   You can unpause it and trigger runs manually from the Airflow UI.

### Alternative: Running Airflow Natively

This method requires installing Airflow and its dependencies directly on your host machine.

1.  **Install dependencies:** Ensure `apache-airflow` and other project requirements are installed (`pip install -r requirements.txt`).
2.  **Set environment variables:** Configure `.env` or export variables in your shell (including `AIRFLOW__CORE__FERNET_KEY`).
3.  **Initialize Airflow Home:**
    ```sh
    export AIRFLOW_HOME=$(pwd)/airflow_home
    airflow db init
    ```
4.  **Create Admin User:**
    ```sh
    airflow users create \
      --username admin --firstname Admin --lastname User \
      --role Admin --email admin@example.com --password admin
    ```
5.  **Start Scheduler & Webserver:**
    ```sh
    airflow scheduler &
    airflow webserver
    ```
6.  **Access UI:** Open [http://localhost:8080](http://localhost:8080) (default Airflow port, might conflict with API if run natively too).

### Customizing the Pipeline
*   **Cities:** Set the `CITIES` env variable (comma-separated) in `.env`.
*   **Schedule:** Set the `PIPELINE_SCHEDULE` environment variable (cron string, e.g. `0 * * * *`, or timedelta string, e.g. `hours=2`) in your `.env` or shell. If not set, defaults to every hour. You can also change `schedule_interval` in `dags/weather_data_pipeline.py`.
*   **Storage:** The pipeline will use GCS or local JSON depending on the `STORAGE_BACKEND` variable in `.env`.

### Testing the Pipeline
*   Unit tests for the DAG logic are provided in `tests/dags/test_weather_data_pipeline.py` (uses mocks for external calls). Run using `pytest` (see Testing section).

### Deploying to Google Cloud Composer
*   To deploy the pipeline to Composer, copy the contents of `/dags` to your Composer environment's DAGs folder and ensure all required dependencies are present in Composer's PyPI dependencies (see `requirements.txt`).

---

## Project Overview

This service provides weather data via a REST API and includes an Airflow pipeline to periodically fetch and store weather statistics for specified cities. It supports both local development (Docker, native Python) and deployment to Google Cloud Platform (using Cloud Run, Cloud Composer, and Cloud Storage).

## Features

*   **REST API:** Provides endpoints to fetch current weather and historical weather statistics.
*   **API Key Authentication:** Secures API endpoints using an API key.
*   **Automated Data Pipeline:** Uses Apache Airflow to periodically fetch weather data for configured cities.
*   **Configurable Storage:** Supports storing weather statistics in local JSON files or Google Cloud Storage.
*   **Infrastructure as Code:** Uses Terraform (`infra/`) to manage Google Cloud resources.
*   **Dockerized Environment:** Simplifies development setup and testing using Docker and Docker Compose.
*   **Unit Tests:** Includes tests for API endpoints, data pipeline logic, and core components.

## Architecture

The project follows a modular structure:

*   **API Server (`src/presentation/api_server.py`):** A simple Python `http.server` based API exposing weather data endpoints.
*   **Data Pipeline (`dags/weather_data_pipeline.py`):** An Apache Airflow DAG responsible for fetching data from an external weather source (implicitly, via use cases) and storing it.
*   **Core Logic (`src/`):**
    *   `use_cases`: Orchestrate application logic (e.g., fetching current weather, retrieving stats).
    *   `domain`: Defines core data structures (e.g., `WeatherRecord`, `WeatherStats`).
    *   `gateways`: Abstracts external interactions (e.g., external weather API, data storage like GCS or local files).
*   **Configuration (`src/config.py`, `.env`):** Manages settings via environment variables.
*   **Storage:** Can use local JSON files (`data/`) or Google Cloud Storage, configured via environment variables.
*   **Infrastructure (`infra/terraform/`):** Terraform code defines GCP resources (Cloud Run for the API, Cloud Composer for Airflow, GCS for storage, supporting IAM and Network resources).

## API Documentation

The API server provides the following endpoints:

*   **Authentication:** All endpoints require an `X-API-Key` header containing the API key defined in the `API_KEY` environment variable. Unauthorized requests will receive a `401` response.

*   **`GET /weather/current/{city}`:**
    *   Retrieves the latest available weather information for the specified `{city}`.
    *   **Success Response (200 OK):** JSON object representing the current weather (structure defined by `src/use_cases/get_current_weather.py`).
    *   **Error Responses:** `400 Bad Request` (if city is missing), `401 Unauthorized`, `404 Not Found` (if city data is unavailable or an internal error occurs).

*   **`GET /weather/stats/{city}`:**
    *   Retrieves historical weather statistics (e.g., average temperature, min/max) for the specified `{city}`.
    *   **Success Response (200 OK):** JSON object representing the weather statistics (structure defined by `src/domain/weather_stats.py` and populated by `src/use_cases/get_weather_stats.py`).
    *   **Error Responses:** `400 Bad Request` (if city is missing), `401 Unauthorized`, `404 Not Found` (if city data is unavailable or an internal error occurs).

*Example Usage (using curl):*
```sh
# Assuming API runs on port 8080 via docker compose or docker run
curl -H "X-API-Key: YOUR_API_KEY" http://localhost:8080/weather/current/London
curl -H "X-API-Key: YOUR_API_KEY" http://localhost:8080/weather/stats/Paris
```

## Configuration

Configuration is managed primarily through environment variables loaded from a `.env` file.

1.  **Create `.env` file:**
    ```sh
    cp .env.example .env
    ```
2.  **Edit `.env`:** Provide values for the required variables:
    *   `API_KEY`: The secret key for API authentication. **Required.**
    *   `CITIES`: Comma-separated list of cities for the data pipeline (e.g., `London,Paris,Berlin`). **Required for pipeline.**
    *   `STORAGE_BACKEND`: `local` or `gcs`. Defaults to `local` if not set.
    *   `GCP_PROJECT_ID`, `GCS_BUCKET_NAME`: Required if `STORAGE_BACKEND=gcs`.
    *   `AIRFLOW__CORE__FERNET_KEY`: **Required for Airflow.** Generate using the command in the Airflow section.
    *   `PIPELINE_SCHEDULE`: Optional cron string (e.g., `0 * * * *`) or timedelta string (e.g., `hours=2`) for the pipeline schedule. Defaults to hourly.
    *   Other Airflow/GCP variables as needed (see `.env.example`).

## Testing

Unit tests are located in the `tests/` directory.

*   **Run tests (Docker Compose Recommended):**
    ```sh
    docker compose run --rm api pytest
    ```
    *   This runs tests in an isolated container using the `api` service definition.

*   **Run tests (Alternative Docker):**
    ```sh
    docker run --rm -it weather-data-service pytest
    ```

*   **Run tests (Native):**
    ```sh
    pytest
    ```

## Infrastructure (Infrastructure as Code)

The `infra/terraform/` directory contains Terraform code to provision the necessary Google Cloud Platform resources for deploying the service. This typically includes:

*   Google Cloud Run service for the API server.
*   Google Cloud Composer environment for the Airflow pipeline.
*   Google Cloud Storage bucket for data storage.
*   Associated IAM roles and permissions.
*   VPC Network configuration (if needed).

Refer to the README within the `infra/terraform/` directory for specific deployment instructions
