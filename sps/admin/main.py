import sqlalchemy as sa
import aiohttp_jinja2

from admin.views import AdminAPIView, AdminGUIView


class Admin:

    app = None
    resources = []

    # This should be singleton, still not sure it is necessary
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '__instance'):
            cls.__instance = super(Admin, cls).__new__(cls)
        return cls.__instance

    @aiohttp_jinja2.template('admin/base_list.html')
    async def base_list(self, request):
        return {}

    @aiohttp_jinja2.template('admin/base_detail.html')
    async def base_detail(self, request):
        return {}

    def __init__(self, app):
        self.app = app
        # Shortcuts for app`s routing
        self.app.router.add_get('/admin/list', self.base_list, name='admin_list')
        self.app.router.add_get('/admin/detail', self.base_detail, name='admin_detail')
        app.router.add_static('/admin-static',
                              '/home/mqtx/projects/sps_async/sps/admin/templates/admin',
                              name='admin-static')

        self.app.router.add_get('/admin', self.admin_home, name='admin-home')

    def register_table(self, table, **kwargs):


        new_admin_resource = AdminResource(
            pool=self.app['pool'],
            table=table,
            key_field=kwargs.pop('key_field', None),
            list_fields=kwargs.pop('list_fields', None),
        )

        new_admin_resource.setup_routes(self.app)
        self.resources.append(new_admin_resource)

    @aiohttp_jinja2.template('admin/base.html')
    async def admin_home(self, request):
        return {}


class AdminResource:

    def __init__(self, pool, table, key_field=None, list_fields=None):
        if not isinstance(table, sa.Table):
            raise TypeError('sqlalchemy.Table instance required to create '
                            'AdminResource, got {} of type {}.'
                            .format(table, type(table)))


        if key_field is None:
            key_field = 'id'
        key_check = getattr(table.columns, key_field, None)
        if not isinstance(key_check, sa.Column):
            raise ValueError(
                'Cannot create AdminResource for {}, bad field {} '
                'passed to key_field.'.format(table.name, key_field)
            )

        if list_fields is None:
            list_fields = [str(column.name) for column in table.columns]
        else:
            available_fields = {str(column.name) for column in table.columns}
            for field in list_fields:
                if field not in available_fields:
                    raise ValueError(
                        'Cannot create AdminResource for {}, bad field {} '
                        'passed to list_display.'.format(table.name, field)
                    )

        self.table = table
        self.key_field = key_field
        self.list_fields = list_fields

        self.create_api(pool)
        self.create_gui(pool)

    def create_api(self, pool):
        self.api_view = AdminAPIView(
            pool=pool,
            table=self.table,
            key_field=self.key_field
        )


    def create_gui(self, pool):
        self.gui_view = AdminGUIView(
            table=self.table,
            key_field=self.key_field,
            list_fields=self.list_fields,
        )

    def setup_routes(self, app):
        # CRUD REST API
        api_name = 'admin-api-' + self.table.name
        api_url = '/admin/api/{}'.format(self.table.name)
        app.router.add_get(api_url, self.api_view.list, name=api_name + '-list')
        app.router.add_get(api_url + '/{key}', self.api_view.retrieve, name=api_name + '-retrieve')
        app.router.add_post(api_url, self.api_view.create, name=api_name + '-create')
        app.router.add_post(api_url + '/{key}', self.api_view.update, name=api_name + '-update')
        app.router.add_delete(api_url + '/{key}', self.api_view.delete, name=api_name + '-delete')

        # GUI INTERFACE TO INTERACT WITH ADMIN API
        gui_name = 'admin-' + self.table.name
        gui_url = '/admin/{}'.format(self.table.name)
        app.router.add_get(gui_url, self.gui_view.list, name=gui_name + '-list')
        app.router.add_get(gui_url + '/new', self.gui_view.new, name=gui_name + '-new')
        app.router.add_get(gui_url + '/{key}', self.gui_view.detail, name=gui_name + '-detail')

