from .main import Admin

def register_in_app(app, prefix=None):
    app['apps'].update({
        'admin': {}
    })
    app.admin = Admin(app=app)
