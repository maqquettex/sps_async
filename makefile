all:
	env/bin/python manage.py

setup:
	virtualenv --python=python3 env
	env/bin/pip install -r requirements.txt
	git clone https://github.com/aio-libs/aiohttp_admin
	cd aiohttp_admin ?? ../env/bin/python aiohttp_admin/setup.py install
	rm aiohttp_admin/ -rf

