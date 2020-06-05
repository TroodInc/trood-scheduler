default: run

build:
	@docker-compose build

test:
	@docker-compose exec scheduler pytest

run: build
	@docker-compose up -d

down:
	@docker-compose down

full-restart:
	@make down
	@docker system prune
	@make build
	@make run
	@sleep 15
	@make test

.PHONY: run default build test down
