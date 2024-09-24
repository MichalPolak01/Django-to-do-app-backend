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

        self.client.post("/register", json = {
            "email": "testuser2@example.com",
            "password": "TestPassword123#",
            "first_name": "John",
            "last_name": "Doe"
        })

        login_response = self.client.post("/login", json = {
            "email": "testuser2@example.com",
            "password": "TestPassword123#",
        })
        self.access_token = login_response.json().get("access")


    def test_successful_registration(self):
        """ Test registration of a new user with valid credentials """

        response = self.client.post("/register", json = {
            "email": "newuser@example.com",
            "password": "NewPassword123$",
            "first_name": "Alice",
            "last_name": "Smith"
        })

        self.assertEqual(response.status_code, 201, "Registration failed with valid credentials")

    
    def test_failed_registration(self):
        """ Test registration with invalid credentials """

        response = self.client.post("/register", json = {
            "email": "invaliduser@example.com",
            "password": "qwe123",
            "first_name": "John",
            "last_name": "Doe"
        })

        self.assertEqual(response.status_code, 400, "Registration succeeded with invalid credentials")


    def test_invalid_email_registration(self):
        """ Test registration with an invalid email format """

        response = self.client.post("/register", json = {
            "email": "invalidemail",
            "password": "ValidPassword123#",
            "first_name": "John",
            "last_name": "Doe"
        })

        self.assertEqual(response.status_code, 422, "Registration succeeded with invalid email format")


    def test_successful_login(self):
        """ Test login with correct user credentials """

        response = self.client.post("/login", json = {
            "email": "testuser@example.com",
            "password": "TestPassword123#",
        })

        self.assertEqual(response.status_code, 200, "Login failed with valid credentials")

        self.assertIn("access", response.json())
        self.assertIn("refresh", response.json())


    def test_failed_login(self):
        """ Test login with incorrect user credentials """

        response = self.client.post("/login", json = {
            "email": "testuser@example.com",
            "password": "WrongPassword123$"
        })

        self.assertEqual(response.status_code, 401, "Login succeeded with invalid credentials")
        self.assertEqual(response.json()["detail"],  "Invalid email or password")


    def test_login_nonexistent_user(self):
        """ Test login with a non-existent user """

        response = self.client.post("/login", json = {
            "email": "nonexistent@example.com",
            "password": "NonExistentPassword123%"
        })

        self.assertEqual(response.status_code, 401, "Login succeeded with a non-existent user")
        self.assertEqual(response.json()["detail"],  "Invalid email or password")


    def test_successful_user_update(self):
        """ Test user profile update with valid credentials """

        response = self.client.put("/user/edit",
            json = {
                "email": "testuser2@example.com",
                "first_name": "Alice",
                "last_name": "Smith"
            }, 
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
        )

        self.assertEqual(response.status_code, 200, "User update failed with valid credentials")
        self.assertIn("first_name", response.json())
        self.assertIn("last_name", response.json())


    def test_update_without_authorization(self):
        """ Test user profile update without authorization token """

        response = self.client.put("/user/edit", json = {
            "email": "testuser2@example.com",
            "first_name": "Alice",
            "last_name": "Smith"
        })

        self.assertEqual(response.status_code, 401, "User update succeeded without authorization")


    def test_duplicate_email_update(self):
        """ Test user profile update with a duplicate email """

        response = self.client.put("/user/edit",
            json = {
                "email": "testuser@example.com",
                "first_name": "John",
                "last_name": "Doe"
            }, 
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
        )

        self.assertEqual(response.status_code, 400, "User update succeeded with duplicate email")


    def test_successful_password_change(self):
        """ Test password change with valid credentials """

        response = self.client.put("/user/change_password", 
            json = {
                "old_password": "TestPassword123#",
                "password": "TestPassword123$"
            },
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
        )
        
        self.assertEqual(response.status_code, 200, "Password change failed with valid credentials")
        self.assertEqual(response.json()["message"], "Password changed successfully")

    
    def test_failed_password_change_due_to_wrong_old_password(self):
        """ Test password change with an incorrect old password """

        response = self.client.put("/user/change_password", 
            json = {
                "old_password": "WrongPassword123%",
                "password": "TestPassword123$"
            },
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
        )
        
        self.assertEqual(response.status_code, 400, "Password change succeeded with an incorrect old password")


    def test_failed_password_change_due_to_invalid_new_password(self):
        """ Test password change with an invalid new password """

        response = self.client.put("/user/change_password", 
            json = {
                "old_password": "TestPassword123#",
                "password": "WrongPassword"
            },
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
        )
        
        self.assertEqual(response.status_code, 400, "Password change succeeded with an invalid new password")