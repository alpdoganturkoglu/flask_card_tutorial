from flask import Flask, render_template
from app.config import DevelopmentConfig, TestingConfig
import os
from flask_login import LoginManager
from app.database import db
from . import cardf
from . import auth


def create_app(test_config=False):
    flask_app = Flask(__name__)
    app_env = os.getenv("FLASK_ENV", DevelopmentConfig.NAME)

    if test_config or app_env == TestingConfig.NAME:
        flask_app.config.from_object(TestingConfig)
    elif app_env == DevelopmentConfig.NAME:
        flask_app.config.from_object(DevelopmentConfig)

    # init db
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DevelopmentConfig.DBPATH
    db.init_app(flask_app)
    with flask_app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.init_app(flask_app)

    # registering user and card blueprints
    flask_app.register_blueprint(cardf.card_bp)
    flask_app.register_blueprint(auth.user_bp)

    login_manager.login_view = 'user.login'

    return flask_app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
