PROJECT_DIR=pwd

all:
	env/bin/python sps/manage.py

build_aiohttp:
	docker build . -t sps/aiohttp

run:
	docker-compose up
