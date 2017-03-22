import jinja2
import aiohttp_jinja2

from .routes import setup_routes
from .db import create_tables_sql, artist, song


def register_in_app(app, prefix=None):
    prefix = prefix.replace('/', '')
    app['apps'].update({
        # api`s app dictionary
        'api': {}
    })
    # If admin sub-app is plugged - use it
    if 'admin' in app['apps']:
        register_in_admin(app.admin)

    setup_routes(app, prefix)
    aiohttp_jinja2.setup(
        app, loader=jinja2.PackageLoader('api', 'templates')
    )
    app.on_startup.append(db.create_tables_sql)


def register_in_admin(admin):
    app_prefix = 'api'

    admin.register_table(
        app_prefix=app_prefix,
        name='songs',
        table=song,
        list_dislay=[song.c.id, song.c.artist_id, song.c.title]
    )

    admin.register_table(
        app_prefix=app_prefix,
        name='artists',
        table=artist,
        list_dislay=[artist.c.id, artist.c.name]
    )
