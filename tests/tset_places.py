
"""
Tests for places endpoints.
"""

import unittest

from app import create_app


class PlaceTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_get_places(self):

        response = self.client.get(
            '/api/v1/places/'
        )

        self.assertEqual(
            response.status_code,
            200
        )


if __name__ == "__main__":
    unittest.main()