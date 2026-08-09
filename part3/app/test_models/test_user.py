```python
import unittest

from ..models.user import User


class TestUser(unittest.TestCase):

    def test_user_creation(self):
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="password123"
        )

        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertFalse(user.is_admin)

        user_id = user.id

        self.assertEqual(
            user.to_dict(),
            {
                "id": user_id,
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com"
            }
        )

    def test_user_max_length(self):
        with self.assertRaises(ValueError) as context:
            User(
                first_name="abdcdefghijklmnopqrstuvwxyzabdcdefghijklmnopqrstuvwxyz",
                last_name="Doe",
                email="john.doe@example.com",
                password="password123"
            )

        self.assertEqual(
            str(context.exception),
            "First name must be 50 characters max."
        )

        with self.assertRaises(ValueError) as context:
            User(
                first_name="John",
                last_name="abdcdefghijklmnopqrstuvwxyzabdcdefghijklmnopqrstuvwxyz",
                email="john.doe@example.com",
                password="password123"
            )

        self.assertEqual(
            str(context.exception),
            "Last name must be 50 characters max."
        )

    def test_user_email(self):
        with self.assertRaises(ValueError) as context:
            User(
                first_name="John",
                last_name="Doe",
                email="john.doeexample.com",
                password="password123"
            )

        self.assertEqual(
            str(context.exception),
            "Invalid email format"
        )

    def test_user_required_fields(self):
        with self.assertRaises(TypeError):
            User(
                first_name="John",
                last_name="Doe"
            )

        with self.assertRaises(TypeError):
            User(
                first_name="John",
                email="john.doe@example.com"
            )

        with self.assertRaises(TypeError):
            User(
                last_name="Doe",
                email="john.doe@example.com"
            )

    def test_user_update(self):
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="password123"
        )

        new_data = {
            "first_name": "Jane",
            "last_name": "Dupont",
            "email": "jane.dupont@example.com"
        }

        user.update(new_data)

        self.assertEqual(
            user.to_dict(),
            {
                "id": user.id,
                "first_name": "Jane",
                "last_name": "Dupont",
                "email": "jane.dupont@example.com"
            }
        )

    def test_user_update_fail(self):
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="password123"
        )

        with self.assertRaises(ValueError) as context:
            user.first_name = (
                "abdcdefghijklmnopqrstuvwxyz"
                "abdcdefghijklmnopqrstuvwxyz"
            )

        self.assertEqual(
            str(context.exception),
            "First name must be 50 characters max."
        )

        with self.assertRaises(ValueError) as context:
            user.last_name = (
                "abdcdefghijklmnopqrstuvwxyz"
                "abdcdefghijklmnopqrstuvwxyz"
            )

        self.assertEqual(
            str(context.exception),
            "Last name must be 50 characters max."
        )

        with self.assertRaises(ValueError) as context:
            user.email = "john.doeexample.com"

        self.assertEqual(
            str(context.exception),
            "Invalid email format"
        )


if __name__ == "__main__":
    unittest.main()
```
