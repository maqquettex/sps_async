import yaml
import pathlib

import jinja2
import aiohttp_jinja2


def detect_config(file_path, trafaret, config_name='config.yaml'):

    dir_to_explore = pathlib.Path(file_path).parent
    conf_path = dir_to_explore / config_name

    with open(conf_path, 'rt') as file:
        config = yaml.load(file)
    trafaret.check(config)

    return config

def setup_jinja2(app, app_file_path):
    base_dir = pathlib.Path(app_file_path).parent
    admin_folder = base_dir / 'admin' / 'templates'
    project_folder = base_dir / 'templates'

    template_folders = [
        str(admin_folder), str(project_folder)
    ]

    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(template_folders)
    )
