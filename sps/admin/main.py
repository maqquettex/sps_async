import sqlalchemy as sa
from .views import AdminAPIView

class Admin:

    app = None

    registered = []

    def __init__(self, app):
        Admin.app = app
        # Shortcuts for app`s routing
        Admin.add_get = app.router.add_get
        Admin.add_post = app.router.add_post
        Admin.add_delete = app.router.add_delete

    def register_table(self, table):
        if not isinstance(table, sa.Table):
            raise TypeError('You must pass sqlalchemy.Table instance to admin`s '
                            'register_table function')
        new_admin_view = AdminAPIView(table=table, pool=self.app['pool'])

        admin_name = 'admin-' + table.name
        base_url = '/admin/{}'.format(table.name)
        self.add_get(base_url, new_admin_view.list, name=admin_name + '-list')
        self.add_get(base_url + '/{key}', new_admin_view.retrieve, name=admin_name + '-retrieve')

        self.add_post(base_url, new_admin_view.create, name=admin_name + '-create')
        self.add_post(base_url + '/{key}', new_admin_view.update, name=admin_name + '-update')

        self.add_delete(base_url, new_admin_view.delete_many, name=admin_name + '-delete-many')
        self.add_delete(base_url + '/{key}', new_admin_view.delete, name=admin_name + '-delete')