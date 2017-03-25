import types
import sqlalchemy as sa
from sqlalchemy.sql import sqltypes
from aiohttp import web

from admin.validations import *


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
                if key.isdigit():
                    return int(key)
                raise web.HTTPNotFound()
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
        req_data = await request.json()
        if not isinstance(req_data, dict):
            return web.HTTPBadRequest()

        insert_values = {}
        for field, f_value in req_data.items():
            # Is field necessary for this table
            if field not in self.field_names:
                continue

            # Is field valid
            try:
                value = validate_field(f_value, getattr(self.fields, field))
            except AdminValidationError:
                import traceback
                traceback.print_exc()
                return web.HTTPBadRequest()
            insert_values.update({
                field: value
            })

        try:
            async with self.pool.transaction() as conn:
                result = await conn.fetchrow(
                    self.table.insert().values(**insert_values)
                )
        except:
            import traceback
            traceback.print_exc()
            return web.HTTPBadRequest()

        return web.json_response({})

    async def update(self, request):
        req_data = await request.json()
        if not isinstance(req_data, dict):
            return web.HTTPBadRequest()

        key_field = self.get_key(request)
        query = self.table.update().where(
            getattr(self.fields, self.key_field) == key_field
        )

        update_values = {}
        for field, f_value in req_data.items():
            # Is field necessary for this table
            if field not in self.field_names:
                continue
            elif field == self.key_field \
                 or getattr(self.fields, field).primary_key:
                return web.json_response(
                    {'error': 'Cannot update key or primary field'}, status=422
                )

            # Is field valid
            try:
                value = validate_field(f_value, getattr(self.fields, field))
            except AdminValidationError:
                import traceback
                traceback.print_exc()
                return web.HTTPBadRequest()
            update_values.update({
                field: value
            })

        try:
            async with self.pool.transaction() as conn:
                result = await conn.fetchrow(
                    query.values(**update_values)
                )
        except:
            import traceback
            traceback.print_exc()
            return web.HTTPBadRequest()

        query = self.table.select().where(
            getattr(self.fields, self.key_field) == key_field
        )

        async with self.pool.transaction() as conn:
            result = await conn.fetchrow(query)

        return web.json_response({
            field: getattr(result, field)
            for field in self.field_names
        })

    async def delete(self, request):
        key_field = self.get_key(request)
        query = self.table.delete().where(
            getattr(self.fields, self.key_field) == key_field
        )

        async with self.pool.transaction() as conn:
            await conn.fetchrow(query)

        return web.json_response({})
