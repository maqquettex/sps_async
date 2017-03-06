import jinja2
import aiohttp_jinja2

from .routes import setup_routes
from .db import create_tables_sql


async def register_in_app(app, prefix=None):
    setup_routes(app, prefix)
    aiohttp_jinja2.setup(
        app, loader=jinja2.PackageLoader('api', 'templates')
    )
    app.on_startup.append(db.create_tables_sql)
