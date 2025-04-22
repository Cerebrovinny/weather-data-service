# Weather Data Service Project: Design Decisions

This document explains the rationale behind the design choices made for the Weather Data Service Project.

## 1. Technology Stack

- **Programming Language: Python 3**
  - Chosen primarily because it was a project requirement. (technical constraint)

- **Orchestration: Apache Airflow**
  - Selected as required for scheduling and managing complex data workflows. (technical constraint)

- **Infrastructure as Code: Terraform**
  - Used for managing infrastructure in GCP as explicitly required. Terraform simplifies resource creation and maintenance. (technical constraint)

- **Cloud Provider: Google Cloud Platform (GCP)**
  - Required by the project's specifications. GCP provides managed services, such as Cloud Run and Cloud Composer, suitable for this project's scale and complexity. (technical constraint)

- **Containerization: Docker & Docker Compose**
  - (Cloud Run uses containers implicitly), Docker is essential for creating reproducible build artifacts and providing a consistent local development environment.

## 2. Architecture

- **Project Structure:** Organized into clear, modular directories:
  - `src/`: Application logic.
  - `dags/`: Airflow pipeline definitions.
  - `infra/`: Terraform scripts.
  - `tests/`: Tests mirroring the application’s structure.

- **Clean Architecture Principles:**
  - `domain`: Core business objects.
  - `use_cases`: Application logic orchestrating domain and external interfaces.
  - `gateways`: Interfaces for external dependencies, allowing flexibility.
  - `presentation`: Manages API endpoints.

- **Simple REST API:**
  - Specified endpoints defined on the requirements (`/weather/current/{city}`, `/weather/stats/{city}`). Designed minimally to suit project scope.

## 3. API Implementation

- **Framework:** Python’s built-in `http.server` was chosen for simplicity and minimal dependencies.

- **Authentication:** Implemented via a simple API key header (`X-API-Key`), available from environment variables.

- **Error Handling:** Uses basic Python error handling.

## 4. Data Storage

- **Abstracted Storage Gateway:** Provides flexibility to switch between different storage solutions without affecting application logic.

- **Implemented Storage Backends:**
  - **Local JSON:** Ideal for local testing without cloud dependencies.
  - **Google Cloud Storage (GCS):** Required by project specs, offering a robust and scalable cloud solution.

- **Configurability:** Storage backend selection via environment variable (`STORAGE_BACKEND`).

- **Data Format:** JSON was chosen for simplicity, I also decide to write the files separated by City this is to avoid concurrency issues when we are writing multiple times into the same resource.

## 5. Data Processing Pipeline

- **Apache Airflow DAG:** 
  - Task structure includes fetching data, transforming it, and storing results.

- **Dynamic Configuration:** Allows easy adjustments of cities and scheduling through environment variables.

## 6. Infrastructure

- **Google Cloud Platform (GCP):**
  - **Cloud Run:** Serverless containerized API deployment.
  - **Cloud Storage:** Data storage and Terraform backend.
  - **Cloud Composer:** Service for Airflow pipelines.

- **Terraform Modules:** Facilitates maintainability and reusability of infrastructure code.

- **State Management:** Terraform backend stored on GCS for reliability and collaboration.

## 7. Continuous Integration and Deployment (CI/CD)

- **GitHub Actions:**
  - Automates code checks, testing, Docker image builds, and deployments, adhering strictly to the project requirements.

## 8. Testing Strategy

- **Framework:** Pytest was chosen for because it's simple to test.

- **Test Types:**
  - **Unit Tests:** Isolate and verify functionality in the domain, business logic, and external interfaces.
  - **Integration Tests:** Verify endpoint functionality and cross-component interactions.
  - **Airflow DAG Tests:** Ensure pipeline integrity.