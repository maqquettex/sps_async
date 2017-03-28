import os
from shutil import copyfile

import aiohttp_jinja2
from aiohttp import web
from functools import wraps

from sqlalchemy.sql import sqltypes






def general_admin_interface(admin_gui_view):
    @wraps(admin_gui_view)
    def wrapper(*args, **kwargs):
        view_specific_context = admin_gui_view(*args, **kwargs)


class AdminGUIView:

    def __init__(self, table, key_field, list_fields):
        self.table = table
        self.table_name = table.name
        templates_path = '/home/mqtx/projects/sps_async/sps/admin/templates/admin'
        try:
            os.stat(templates_path + '/' + self.table_name)
        except:
            os.mkdir(templates_path + '/' + self.table_name)

        copyfile(templates_path + '/base_detail.html',
                 templates_path + '/' + self.table_name + '/detail.html')

        copyfile(templates_path + '/base_list.html',
                 templates_path + '/' + self.table_name + '/list.html')

        self.list = aiohttp_jinja2.template(
            'admin/' + self.table_name + '/list.html'
        )(self.list)

        self.new = aiohttp_jinja2.template(
            'admin/' + self.table_name + '/detail.html'
        )(self.new)

        self.detail = aiohttp_jinja2.template(
            'admin/' + self.table_name + '/detail.html'
        )(self.detail)

    async def list(self, request):
        fields = []
        for col in self.table.columns:
            if isinstance(col.type, sqltypes.Integer):
                print(col.name, 'is int')
            elif isinstance(col.type, sqltypes.Text):
                print(col.name, 'is text')
            elif isinstance(col.type, sqltypes.String):
                print(col.name, 'is str')
            else:
                raise TypeError('Unsupported type of shit.')
        return {
            'fields': [

            ]
        }

    async def new(self, request):
        return {}

    async def detail(self, request):
        return {}

