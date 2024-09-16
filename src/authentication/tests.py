from django.test import TestCase
from ninja.testing import TestClient
from .api import router


class NinjaAuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = TestClient(router)

        self.client.post("/register", json = {
            "email": "testuser@example.com",
            "password": "TestPassword123#",
            "first_name": "John",
            "last_name": "Doe"
        })


    def test_register_success(self):
        """ Success register test for new user """

        response = self.client.post("/register", json = {
            "email": "newuser@example.com",
            "password": "NewPassword123$",
            "first_name": "Alice",
            "last_name": "Smith"
        })

        self.assertEqual(response.status_code, 201, "Registration failed with valid credentials")

    
    def test_register_failure(self):
        """ Register test with incorrect credentials """

        response = self.client.post("/register", json = {
            "email": "invaliduser@example.com",
            "password": "qwe123",
            "first_name": "John",
            "last_name": "Doe"
        })

        self.assertEqual(response.status_code, 400, "Registration success with invalid credentials")


    def test_register_invalid_email(self):
        """ Register test with invalid email format """
        response = self.client.post("/register", json = {
            "email": "invalidemail",
            "password": "ValidPassword123#",
            "first_name": "John",
            "last_name": "Doe"
        })
        self.assertEqual(response.status_code, 422, "Registration succeeded with invalid email format")


    def test_login_success(self):
        """ Login test user with coorrect credentials """

        response = self.client.post("/login", json = {
            "email": "testuser@example.com",
            "password": "TestPassword123#",
        })

        self.assertEqual(response.status_code, 200, "Login failed with valid credentials")

        self.assertIn("access", response.json())
        self.assertIn("refresh", response.json())


    def test_login_failure(self):
        """ Login test user with incorrect credentials """

        response = self.client.post("/login", json = {
            "email": "testuser@example.com",
            "password": "WrongPassword123$"
        })

        self.assertEqual(response.status_code, 401, "Login success with invalid credentials")
        self.assertEqual(response.json()["detail"],  "Invalid email or password")


    def test_login_non_existing_user(self):
        """ Login test with non existing user """

        response = self.client.post("/login", json = {
            "email": "nonexistent@example.com",
            "password": "NonExistentPassword123%"
        })

        self.assertEqual(response.status_code, 401, "Login success with non existing user")
        self.assertEqual(response.json()["detail"],  "Invalid email or password")