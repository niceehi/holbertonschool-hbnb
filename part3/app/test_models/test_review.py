```python
import unittest

from ..models.review import Review


class TestReview(unittest.TestCase):

    def test_review_creation(self):
        review = Review(name="Wi-Fi")
        self.assertEqual(review.name, "Wi-Fi")


if __name__ == "__main__":
    unittest.main()
```
