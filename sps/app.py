import os
import asyncio
import asyncpgsa
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
    db_config = utils.conf.get_db_config()
    print(db_config)
    # saving config
    app['conf'] = {'postgres': db_config}
    app['pool'] = await asyncpgsa.create_pool(**db_config)

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
    print(
        os.getenv('SERVER_HOST', '127.0.0.1'),
        int(os.getenv('SERVER_PORT', 4000))
    )
    web.run_app(app,
                host=os.getenv('SERVER_HOST', '127.0.0.1'),
                port=int(os.getenv('SERVER_PORT', 4000)))

if __name__ == '__main__':
    main()