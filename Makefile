# Makefile for weather-data-service

.PHONY: build run test shell compose-up compose-down clean

build:
	docker build -t weather-data-service .

run:
	docker run --rm -it -p 8080:8080 weather-data-service

test:
	docker run --rm -it weather-data-service pytest

lint:
	docker run --rm -it weather-data-service pylint src tests

shell:
	docker run --rm -it weather-data-service /bin/sh

compose-up:
	docker compose up --build

compose-down:
	docker compose down

clean:
	docker system prune -f
