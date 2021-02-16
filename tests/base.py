import unittest
from app import create_app, db
from app.models.user import User

class BaseTest(unittest.TestCase):

    def_user = {'email': 'test@test.com', 'password': 'test123'}

    def setUp(self):
        self.app = create_app(test_config=True)
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        self.client = self.app.test_client(use_cookies=True)
        db.app = self.app
        db.create_all()
        User.register(email='test@test.com', password='test123')

    def tearDown(self) -> None:
        db.drop_all()
        self.app_ctx.pop()