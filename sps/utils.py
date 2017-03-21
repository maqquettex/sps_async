import yaml
import pathlib
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


def detect_config(file_path, trafaret, config_name='config.yaml'):

    dir_to_explore = pathlib.Path(file_path).parent
    conf_path = dir_to_explore / config_name

    with open(conf_path, 'rt') as file:
        config = yaml.load(file)
    trafaret.check(config)

    return config
