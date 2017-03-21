PROJECT_DIR=pwd

all:
	env/bin/python sps/manage.py

setup_dev:
	virtualenv --python=python3 env
	env/bin/pip install -r requirements.txt
	ln -s $PROJECT_DIR/configs/develop $PROJECT_DIR/sps/config.py

