import unittest
from flask import url_for
from app import app


class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_userhome_route(self):
        response = self.app.get("/userhome")
        self.assertEqual(response.status_code, 302)

    def test_register_route(self):
        response = self.app.get("/register")
        self.assertEqual(response.status_code, 200)

    def test_valid_login(self):
        with self.app as client:
            response = client.post(
                "/userhome",
                data={"username": "stinkycat", "password": "stinkycat"},
                follow_redirects=True,
            )
            self.assertEqual(response.status_code, 200)


def test_logout(self):
    with self.app as client:
        with client.session_transaction() as sess:
            sess["userdata"] = {"username": "test_user"}

        response = client.get("/logout", follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, url_for("index"))
        self.assertNotIn(b"test_user", session.get("userdata", {}))
        self.assertIn(b"USER:test_user - EVENT:logout", response.data)


if __name__ == "__main__":
    unittest.main()
