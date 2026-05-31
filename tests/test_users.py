
"""
Tests for users endpoints.
"""

import unittest

from app import create_app


class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):

        response = self.client.post(
            '/api/v1/users/',
            json={
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@mail.com",
                "password": "123456"
            }
        )

        self.assertEqual(
            response.status_code,
            201
        )

    def test_get_users(self):

        response = self.client.get(
            '/api/v1/users/'
        )

        self.assertEqual(
            response.status_code,
            200
        )


if __name__ == "__main__":
    unittest.main()