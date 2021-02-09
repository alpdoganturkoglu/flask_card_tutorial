from flask import Flask
from app.config import DevelopmentConfig, TestingConfig
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)


# init db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DevelopmentConfig.DBPATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login'