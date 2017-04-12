from .db import create_tables_sql


def register_in_app(app):
    app['apps'].update({
        # api`s app dictionary
        'api': {}
    })

    app.on_startup.append(db.create_tables_sql)