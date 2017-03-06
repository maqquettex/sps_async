import asyncio
import uvloop
from aiohttp import web
from asyncpgsa import pg

import api
import utils


async def init_application(loop):
    config = await utils.load_config()

    await pg.init(**config['postgres'])

    middlewares = [
        # List of middlewares is here
        utils.trailing_slash_redirect_middleware,
    ]

    app = web.Application(loop=loop, middlewares=middlewares)

    await api.register_in_app(app, prefix='/api')
    app['host'] = config['host']
    app['port'] = config['port']
    return app

def main():
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    app = loop.run_until_complete(init_application(loop))

    web.run_app(app, host=app['host'], port=app['port'])
