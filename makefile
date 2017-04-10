PROJECT_DIR=$(shell pwd)
POSTGRES_USER=sps_admin
POSTGRES_PASSWORD=djangochannels
POSTGRES_DB=sps
POSTGRES_HOST=docker_db

all:
	docker-compose up -d
	@sleep 3
	docker-compose up --build -d aiohttp

up:
	docker-compose up -d
	@sleep 3
	docker-compose restart aiohttp
	docker-compose logs -f aiohttp

restart:
	docker-compose restart aiohttp

stop:
	docker-compose stop

conf_dev:
	cp $(PROJECT_DIR)/configs/dev/docker-compose.yml $(PROJECT_DIR)/docker-compose.yml
	cp $(PROJECT_DIR)/configs/dev/Dockerfile $(PROJECT_DIR)/Dockerfile
	cp $(PROJECT_DIR)/configs/dev/environment $(PROJECT_DIR)/environment

link_dev:
	ln $(PROJECT_DIR)/configs/dev/docker-compose.yml $(PROJECT_DIR)/docker-compose.yml
	ln $(PROJECT_DIR)/configs/dev/Dockerfile $(PROJECT_DIR)/Dockerfile
	ln $(PROJECT_DIR)/configs/dev/environment $(PROJECT_DIR)/environment

conf_prod:
	cp $(PROJECT_DIR)/configs/prod/docker-compose.yml $(PROJECT_DIR)/docker-compose.yml
	cp $(PROJECT_DIR)/configs/prod/Dockerfile $(PROJECT_DIR)/Dockerfile
	cp $(PROJECT_DIR)/configs/prod/postgres.env $(PROJECT_DIR)/postgres.env

dump:
	docker-compose exec db pg_dump $(POSTGRES_DB) -U $(POSTGRES_USER) > sps-$(shell date +%Y-%m-%d-%H:%M:%S).sql

dump_init:
	docker-compose exec db pg_dump $(POSTGRES_DB) -U $(POSTGRES_USER) > init_data_v2.sql

clean:
	docker-compose stop
	docker-compose rm -vf
	docker rmi $(docker images | grep "^<none>" | awk "{print $3}")
