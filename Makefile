
mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(patsubst %/,%,$(dir $(mkfile_path)))

.PHONY: up db-up logs stop

up:
	docker compose up -d

db-up:
	docker compose up -d mysql

logs:
	docker-compose logs -f --tail=100

stop:
	docker compose stop
