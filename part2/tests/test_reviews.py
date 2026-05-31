
"""
Tests for reviews endpoints.
"""

import unittest

from app import create_app


class ReviewTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_get_reviews(self):

        response = self.client.get(
            '/api/v1/reviews/'
        )

        self.assertEqual(
            response.status_code,
            200
        )


if __name__ == "__main__":
    unittest.main()