import asyncio
import asyncpgsa
import trafaret as tr
from aiohttp import web

import api
import utils
from utils import admin as admin_utils


async def init_application(loop):
    # SECTION: Creating Application instance, basic init configuration
    middlewares = [
        # List of middlewares is here
        utils.middlewares.trailing_slash_redirect_middleware,
    ]
    app = web.Application(loop=loop, middlewares=middlewares)

    # SECTION: Configuring project
    ipv4_regex = r'^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$'
    PROJECT_CONFIG_TRAFARET = tr.Dict({
        tr.Key('postgres'):
            tr.Dict({
                'user': tr.String(),
                'password': tr.String(),
                'database': tr.String(),
                'host': tr.String(),
                'port': tr.Int(),
            }),
        # regex for ipv4 address
        tr.Key('host'): tr.String(regex=ipv4_regex),
        tr.Key('port'): tr.Int(),
    })
    config = utils.conf.detect_config(__file__, PROJECT_CONFIG_TRAFARET)

    # saving config
    app['conf'] = config
    app['pool'] = await asyncpgsa.create_pool(**config['postgres'])

    # SECTION: sub-apps
    app['apps'] = {}  # dictionary for apps to store any info at
    # Registering apps
    api.register_in_app(app, prefix='api')

    utils.setup_jinja2(app, __file__)
    admin = await admin_utils.get_admin_subapp(app, loop)
    app.add_subapp('/admin', admin)

    return app

def main():
    loop = asyncio.get_event_loop()

    app = loop.run_until_complete(init_application(loop))
    web.run_app(app,
                host=app['conf']['host'],
                port=app['conf']['port'])

if __name__ == '__main__':
    main()