import asyncio
import asyncpgsa
import uvloop

from aiohttp import web

import api
import utils


async def init_application(loop):
    middlewares = [
        # List of middlewares is here
        utils.trailing_slash_redirect_middleware,
    ]

    app = web.Application(loop=loop, middlewares=middlewares)
    config = utils.load_config()
    app['conf'] = config
    app['pool'] = await asyncpgsa.create_pool(**config['postgres'])

    # Registering apps
    api.register_in_app(app, prefix='/api')

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