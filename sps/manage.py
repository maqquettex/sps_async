import asyncio
from asyncpgsa import pg

from aiohttp import web

import api
from utils import *


async def init(loop):
    config = await load_config()

    await pg.init(**config['postgres'])

    middlewares = [
        trailing_slash_redirect_middleware
    ]
    app = web.Application(loop=loop, middlewares=middlewares)

    await api.register_in_app(app, prefix='/api')
    return app

def main():
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init(loop))

    web.run_app(app, host='0.0.0.0', port=4000)


if __name__ == '__main__':
    main()