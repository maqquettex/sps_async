from aiohttp import web


class BaseAdminView:
    pass

async def hello_admin(request):
    return web.json_response({'ok':'true'})