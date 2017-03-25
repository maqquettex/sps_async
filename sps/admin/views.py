import types
import sqlalchemy as sa
from sqlalchemy.sql import sqltypes
from aiohttp import web

from api.db import song, artist


class AdminAPIView:

    def __init__(self, table, pool, key_field):
        self.table = table
        self.pool = pool
        self.fields = self.table.columns
        self.field_names = [str(f.name) for f in self.fields]
        self.key_field = key_field

        # Assigning get_key function
        key_type = getattr(self.fields, self.key_field).type
        if isinstance(key_type, sqltypes.Integer):
            def get_key(request):
                key = request.match_info['key']
                return int(key)
        elif isinstance(key_type, sqltypes.Text):
            def get_key(request):
                key = request.match_info['key']
                return str(key)
        elif isinstance(key_type, sqltypes.String):
            def get_key(request):
                key = request.match_info['key']
                if len(key) < key_type.length:
                    return str(key)
                # Key is longer that man length of field
                raise web.HTTPNotFound()
        else:
            raise ValueError(
                'Unsupported type {} of key field for table {}'.format(
                    key_type, self.table
                )
            )
        self.get_key = get_key

    async def list(self, request):
        query = self.table.select()
        results = []
        async with self.pool.acquire() as conn:
            for row in await conn.fetch(query):
                single_result = {
                    field: getattr(row, field)
                    for field in self.field_names
                }
                results.append(single_result)

        return web.json_response(results)

    async def retrieve(self, request):
        key_field = self.get_key(request)
        query = self.table.select().where(
            getattr(self.fields, self.key_field)==key_field
        )

        async with self.pool.transaction() as conn:
            result_row = await conn.fetchrow(query)

        if not result_row:
            return web.HTTPNotFound()

        return web.json_response({
            field: getattr(result_row, field)
            for field in self.field_names
        })

    async def create(self, request):
        print('create', request.match_info)
        print(await request.json())
        return web.json_response({})

    def update(self, request):
        print('update', request.match_info)
        return web.json_response({})

    async def delete(self, request):
        print('delete', request.match_info)
        return web.json_response({})

    async def delete_many(self, request):
        print('delete many', request.match_info)
        return web.json_response({})
