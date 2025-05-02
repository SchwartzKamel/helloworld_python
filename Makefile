.PHONY: test build run clean

test:
	pytest -v --cov=app --cov-report=term-missing

docker-up:
	docker compose up --build

docker-down:
	docker compose down

build:
	docker build -t helloworld:latest .

run:
	docker run -p 8000:8000 helloworld:latest

clean:
	docker rmi helloworld:test helloworld:latest