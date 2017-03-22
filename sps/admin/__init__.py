import jinja2
import aiohttp_jinja2

from .main import AdminInterface


def register_admin(app, prefix=None):
    Admin = AdminInterface(router=app.router)
    app['apps'].update({
        'admin': Admin
    })

    # Just a short cut for admin sub-app
    # Yeah, that`s because ADMIN APP IS CHOSEN ONE!1!
    app.admin = Admin

    aiohttp_jinja2.setup(
        app, loader=jinja2.PackageLoader('admin', 'templates')
    )

def initialize():
    AdminInterface.create_views()