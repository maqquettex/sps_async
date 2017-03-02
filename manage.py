import asyncio

from aiohttp import web

import api


async def init(loop):
    app = web.Application(loop=loop)

    api.register_in_app(app, prefix='/api')
    return app

def main():
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init(loop))
    web.run_app(app, host='0.0.0.0', port=4000)


if __name__ == '__main__':
    main()