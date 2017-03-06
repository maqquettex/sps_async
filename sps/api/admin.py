from pathlib import Path

from . import db
from aiohttp_admin.layout_utils import generate_config


def register_admin_namespace(prefix=None):

    base_url = '/admin'
    if prefix is not None:
        base_url = prefix + base_url

    entities = [
        ("artist", "id", db.artist),
        ("song", "id", db.song),
    ]

    config_str = generate_config(entities, base_url)
    path = Path(__file__).parent.absolute()

    config_location = path / 'static/js/config2.js'
    with open(str(config_location), 'w') as f:
        f.write(config_str)