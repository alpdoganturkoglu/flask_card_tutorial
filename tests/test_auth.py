import unittest
from app import create_app, db
from app.models import User
from flask import url_for, request
from flask_login import current_user


class AuthTest(unittest.TestCase):
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

    def test_login(self):
        with self.client as client:
            # get login page
            resp = client.get('/login')
            self.assertEqual(resp.status_code, 200)
            self.assertTrue('<h1 align="center">Login</h1>' in resp.get_data(as_text=True))

            # try to login
            def_user = {'email': 'test@test.com', 'password': 'test123'}
            resp = client.post('/login', data=def_user, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertTrue(current_user.is_authenticated)
            self.assertTrue('<h1 align="center">Cards</h1>' in resp.get_data(as_text=True))

    def test_login_false(self):
        with self.client as client:

            # try to login
            def_user = {'email': 'test@test.com', 'password': '1234'}
            resp = client.post('/login', data=def_user, follow_redirects=True)
            self.assertEqual(resp.status_code, 400)
            self.assertFalse(current_user.is_authenticated)
            # not redirects
            # self.assertTrue('<h1 align="center">Login</h1>' in resp.get_data(as_text=True))

    def test_register(self):
        with self.client as client:
            # get register page
            resp = client.get('/register')
            self.assertEqual(resp.status_code, 200)

            # register user
            test_user = {'email': 'test2@test.com', 'password': 'test123', 'password2': 'test123'}

            resp = client.post('/register', data=test_user, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertTrue('<h1 align="center">Login</h1>' in resp.get_data(as_text=True))


    def test_logout(self):
        with self.client as client:

            #First sign in
            resp = client.post('/login', data={'email': 'test@test.com', 'password': 'test123'}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertTrue(current_user.is_authenticated)

            # then test logout
            resp = client.get('/logout', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertFalse(current_user.is_authenticated)

