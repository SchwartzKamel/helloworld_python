build:
	docker build -t sierrahackingco/helloworld_python:latest .

test:
	docker run --name helloworld_python sierrahackingco/helloworld_python:latest

help:
	@echo "build test"