import jinja2
import aiohttp_jinja2
from .routes import setup_routes

def register_in_app(app, prefix=None):
    app['apps'].update({
        'admin': {}
    })
    setup_routes(app, prefix)

    # Just a short cut for admin sub-app
    # Yeah, that`s because ADMIN APP IS CHOSEN ONE!1!
