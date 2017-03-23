from .views import SongsAdminView

def setup_routes(app, prefix=None):
    SongsAdminView.add_routes(app, prefix)