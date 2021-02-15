from flask import Flask, redirect
from .models.user import User
from app.config import DevelopmentConfig, TestingConfig
from flask_migrate import Migrate, MigrateCommand
from .routes import init_routes
from flask_script import Manager
from .models import db
from .auth import login_manager


def create_app(test_config=None):

    app = Flask(__name__)
    if test_config is None:
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(TestingConfig)

    db.init_app(app)
    migrate = Migrate(app, db)

    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    init_routes(app)

    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)




