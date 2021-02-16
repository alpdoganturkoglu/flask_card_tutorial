import unittest
from app import create_app, db
from app.models import User
from flask import url_for, request
from flask_login import current_user
from tests.base import BaseTest

class AuthTest(BaseTest):

    def test_login(self):
        with self.client as client:

            # get login page
            resp = client.get('/login')
            self.assertEqual(resp.status_code, 200)
            self.assertTrue('<h1 align="center">Login</h1>' in resp.get_data(as_text=True))

            # try to login
            resp = client.post('/login', data=self.def_user, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertTrue(current_user.is_authenticated)
            self.assertTrue('<h1 align="center">Cards</h1>' in resp.get_data(as_text=True))

    def test_login_wrong_password(self):
        with self.client as client:

            # try to login
            wrong_user = {'email': 'test@test.com', 'password': '1234'}
            resp = client.post('/login', data=wrong_user, follow_redirects=True)
            self.assertEqual(resp.status_code, 400)
            self.assertFalse(current_user.is_authenticated)
            # not redirects
            # self.assertTrue('<h1 align="center">Login</h1>' in resp.get_data(as_text=True))

    def test_login_wrong_user(self):
        with self.client as client:

            # try to login
            wrong_user = {'email': 'test@test.com', 'password': '1234'}
            resp = client.post('/login', data=wrong_user, follow_redirects=True)
            self.assertEqual(resp.status_code, 400)
            self.assertFalse(current_user.is_authenticated)

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

    def test_register_false(self):
        with self.client as client:
            # register user
            test_user = {'email': 'test.com', 'password': 'test123', 'password2': 'test123'}

            resp = client.post('/register', data=test_user, follow_redirects=True)
            self.assertEqual(resp.status_code, 400)



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

