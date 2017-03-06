PROJECT_DIR=pwd

all:
	env/bin/python sps/manage.py

setup:
	virtualenv --python=python3 env
	env/bin/pip install -r requirements.txt
	git clone https://github.com/aio-libs/aiohttp_admin
	cd aiohttp_admin && ../env/bin/python setup.py install
	rm aiohttp_admin/ -rf
	ln -s $PROJECT_DIR/configs/develop $PROJECT_DIR/sps/config.py

