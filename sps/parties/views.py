import json
from aiohttp import web
from aioredis import create_connection

from . import db


def own_dumps(*args, **kwargs):
    kwargs['ensure_ascii'] = False
    return json.dumps(*args, **kwargs)



async def create_party(request):
    tokens = await db.get_party_by_password(
        pool=request.app['pool'], password=request.match_info['password']
    )
    if tokens is not None:
        return web.json_response({'token': ''}, dumps=own_dumps)

    tokens = await db.create_party_by_password(
        pool=request.app['pool'], password=request.match_info['password']
    )
    request.app['apps']['parties'].update({
        request.match_info['password']: []
    })

    return web.json_response(
        {'token': tokens['master_token']},
        dumps=own_dumps
    )


async def register_in_party(request):
    tokens = await db.get_party_by_password(
        pool=request.app['pool'], password=request.match_info['password']
    )
    if tokens is None:
        return web.json_response({'token': ''}, dumps=own_dumps)

    return web.json_response(
        {'token': tokens['user_token']},
        dumps=own_dumps
    )


async def websocket_handler(request):
    ws = web.WebSocketResponse(autoclose=False)
    await ws.prepare(request)

    token_info = await db.get_party_by_token(
        request.app['pool'], token=request.match_info['token']
    )

    if token_info is None:
        await ws.close()
        return ws

    redis = request.app['redis']
    party_key = 'party:{}'.format(token_info['password'])
    party_waiters = request.app['apps']['parties'][token_info['password']]
    party_waiters.append(ws)

    try:
        async for msg in ws:
            if msg.tp == web.MsgType.text:
                print(msg.data, 'got from websocket')


                for waiter in party_waiters:
                    waiter.send_str(msg.data)

            elif msg.tp == web.MsgType.error:
                print('connection closed with exception {}'.format(ws.exception()))
    finally:
        if ws in party_waiters:
            await ws.close()
            party_waiters.remove(ws)

    return ws



