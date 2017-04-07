import os
import pathlib

import jinja2
import aiohttp_jinja2


def get_db_config():
    return {
        'user': os.getenv('POSTGRES_USER', 'postgres'),
        'password': os.getenv('POSTGRES_PASSWORD', ''),
        'host': os.getenv('POSTGRES_HOST', 'localhost'),
        'port': os.getenv('POSTGRES_PORT', 5432),
        'database': os.getenv('POSTGRES_DB', 'sps'),
    }


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
