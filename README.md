# weather-data-service

## Quick Start: Docker Development

This project is designed for reproducible, containerized development. You do **not** need to install Python or dependencies locally—just use Docker!

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

## Project Overview

(Documentation sections to be added: architecture, API, pipeline, etc.)