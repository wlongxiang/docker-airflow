PHONY: run build

TAG=wlongxiang/docker-airflow
VERSION=0.1

build:
	docker build --rm -t ${TAG}:${VERSION} .

push: build
	docker push ${TAG}:${VERSION}

run: build
	docker run -d -p 8080:8080 ${TAG}:${VERSION}
	@echo airflow running on http://localhost:8080

kill:
	@echo "Killing docker-airflow containers"
	docker kill $$(docker ps -q --filter ancestor=${TAG}:${VERSION})

tty:
	@echo running interactive shell...
	docker exec -i -t $$(docker ps -q --filter ancestor=${TAG}:${VERSION}) /bin/bash

compose:
	@echo running docker-compose with local executor
	docker-compose -f docker-compose-LocalExecutor.yml up -d

down:
	@echo running docker-compose with local executor
	docker-compose -f docker-compose-LocalExecutor.yml down
