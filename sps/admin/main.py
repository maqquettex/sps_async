import sqlalchemy as sa
from collections import namedtuple

from .views import hello_admin

TableRecord = namedtuple('TableRecord', ['name', 'table', 'url', 'options'])

class AdminInterface:

    tables = []
    router = None

    def __init__(self, router):
        # Yeah, seriously, save link to router
        AdminInterface.router = router


    @staticmethod
    def register_table(app_prefix, name, table, **kwargs):
        if not isinstance(table, sa.Table):
            raise TypeError('register_tables must take sa.Table`s as arguments!')

        url_template = '/{}/{}'
        new_record = TableRecord(
            name=name,
            table=table,
            url=url_template.format(app_prefix, name),
            options=kwargs
        )

        AdminInterface.tables.append(new_record)


    @staticmethod
    def create_views():
        AdminInterface.router.add_get('/admin', hello_admin, name='test-admin')
        print('creating admin views')



