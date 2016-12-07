#!flask/bin/python
import os
import unittest

from app import flask_app as app
from app import db


class TestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index_redirect(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 302, "Index page is not redirected")

    def test_login_page_live(self):
        resp = self.app.get('/login')
        self.assertEqual(resp.status_code, 200, "Server is not running")

    def login(self, email, password):
        return self.app.post('/login', data=dict(
            email=email,
            password=password
        ))

    def logout(self):
        self.app.get('/logout')

    def test_login_fail(self):
        resp = self.login("a@a.com", "aaaaa")
        self.assertIn(b'Wrong email or password', resp.data, "Login didn't fail")

    def test_register_fail(self):
        resp = self.app.post('/register', data=dict(
            email="a@a.com",
            password="aaaaa"
        ))
        self.assertIn(b'Invalid form', resp.data, "Register didn't fail as expected")

    def register(self):
        return self.app.post('/register', data=dict(
            email="a@a.com",
            password="aaaaa",
            name="Onur",
            birthday="11-11-1991",
            weight="88",
            height="188",
            gender="M",
            notes="asd"
        ), follow_redirects=False)

    def test_register_success(self):
        resp = self.register()
        self.assertEqual(resp.status_code, 302, "Not redirecting after register")
        self.assertIn('/userarea', resp.location, "Not redirecting to userarea")

    def test_login_success(self):
        self.register()
        self.logout()
        resp = self.login("a@a.com", "aaaaa")
        self.assertEqual(resp.status_code, 302, "Login didn't redirect")

if __name__ == '__main__':
    unittest.main()






















