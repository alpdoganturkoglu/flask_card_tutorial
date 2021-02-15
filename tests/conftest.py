import pytest
from app import create_app
from app.models import db


@pytest.fixture
def app():
    app = create_app(test_config=True)
    db.init_app(app)
    db.create_all()
    yield app

    db.session.remove()
    db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


