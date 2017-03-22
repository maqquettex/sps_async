import asyncio
import asyncpgsa
import uvloop
import trafaret as tr
from aiohttp import web

import api
import admin
import utils


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
    admin.register_admin(app, prefix='admin')
    api.register_in_app(app, prefix='api')

    admin.initialize()
    return app

def main():
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)

    app = loop.run_until_complete(init_application(loop))
    web.run_app(app,
                host=app['conf']['host'],
                port=app['conf']['port'])

if __name__ == '__main__':
    main()