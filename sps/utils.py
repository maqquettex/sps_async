import yaml
from aiohttp import web


async def trailing_slash_redirect_middleware(app, handler):
    async def redirect_handler(request):
        if request.path.endswith('/'):

            redirect_url = request.path[:-1]
            # redirecting with GET-params of origin url
            if request.query_string:
                redirect_url += '?' + request.query_string

            return web.HTTPFound(redirect_url)
        return await handler(request)
    return redirect_handler


async def load_config():
    with open('sps/config.yaml', 'rt') as file:
        config = yaml.load(file)
    return config
