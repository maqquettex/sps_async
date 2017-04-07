PROJECT_DIR=pwd
POSTGRES_USER=sps_admin
POSTGRES_PASSWORD=djangochannels
POSTGRES_DB=sps
POSTGRES_HOST=docker_db

all:
	docker-compose up --build -d

stop:
	docker-compose stop

link_dev:
	ln -s $(PROJECT_DIR)/configs/docker-compose.dev.yml $(PROJECT_DIR)/docker-compose.yml

link_prod:
	ln -s $(PROJECT_DIR)/configs/docker-compose.prod.yml $(PROJECT_DIR)/docker-compose.yml

dump_db:
	docker-compose exec db pg_dump $(POSTGRES_DB) -U $(POSTGRES_USER) > sps-$(shell date +%Y-%m-%d-%H:%M:%S).sql
