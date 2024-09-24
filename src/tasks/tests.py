from django.test import TestCase
from ninja.testing import TestClient
from .api import router as tasks_router
from authentication.api import router as auth_router
from django.contrib.auth.models import User

class NinjaAuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = TestClient(tasks_router)
        self.auth_client = TestClient(auth_router)

        self.auth_client.post("/register", json = {
            "email": "testuser@example.com",
            "password": "TestPassword123#",
            "first_name": "John",
            "last_name": "Doe"
        })

        login_response = self.auth_client.post("/login", json = {
            "email": "testuser@example.com",
            "password": "TestPassword123#",
        })
        self.access_token = login_response.json().get("access")
        

    def test_successful_create_task(self):
        """ Test create task with valid data """

        response = self.client.post("",
        json = {
            "title": "Finish project documentation",
            "label": "Documentation",
            "description": "Complete the documentation for the project before the deadline.",
            "status": "backlog",
            "estimated_time": "01:30:00",
            "execution_time": "00:45:00",
            "importance": "high"
        }, 
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        })

        self.assertEqual(response.status_code, 201, "Task add failed with valid data")


    def test_failed_create_task(self):
        """ Test create task with invalid data """

        response = self.client.post("",
        json = {
            "title": "Finish project documentation",
            "label": "Documentation",
        }, 
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        })

        self.assertEqual(response.status_code, 422, "Task add succeded with invalid credentials")


    def test_create_task_without_authorization(self):
        """ Test create task without authorization token"""

        response = self.client.post("",
        json = {
            "title": "Finish project documentation",
            "label": "Documentation",
            "description": "Complete the documentation for the project before the deadline.",
            "status": "backlog",
            "estimated_time": "01:30:00",
            "execution_time": "00:45:00",
            "importance": "high"
        })

        self.assertEqual(response.status_code, 401, "Task add succeded without authorization")


    def test_successful_get_tasks(self):
        """ Test get tasks with existing tasks """

        self.client.post("",
        json = {
            "title": "Finish project documentation",
            "label": "Documentation",
            "description": "Complete the documentation for the project before the deadline.",
            "status": "backlog",
            "estimated_time": "01:30:00",
            "execution_time": "00:45:00",
            "importance": "high"
        }, 
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        })


        response = self.client.get("", headers = {
            "Authorization": f"Bearer {self.access_token}"
        })

        self.assertEqual(response.status_code, 200, "Task get failed with existing tasks")


    def test_failed_get_tasks(self):
        """ Test get tasks without existing tasks """

        response = self.client.get("", headers = {
            "Authorization": f"Bearer {self.access_token}"
        })

        self.assertEqual(response.status_code, 404, "Task get suceded without existing tasks")


    def test_successful_get_task(self):
        """ Test get task with existing task """

        self.client.post("",
        json = {
            "title": "Finish project documentation",
            "label": "Documentation",
            "description": "Complete the documentation for the project before the deadline.",
            "status": "backlog",
            "estimated_time": "01:30:00",
            "execution_time": "00:45:00",
            "importance": "high"
        }, 
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        })


        response = self.client.get("/1", headers = {
            "Authorization": f"Bearer {self.access_token}"
        })

        self.assertEqual(response.status_code, 200, "Task get failed with existing task")


    def test_failed_get_task(self):
        """ Test get task without existing task """

        response = self.client.get("/1", headers = {
            "Authorization": f"Bearer {self.access_token}"
        })

        self.assertEqual(response.status_code, 404, "Task get suceded without existing task")


    def test_successful_update_task(self):
        """ Test update task with existing task """

        self.client.post("",
        json = {
            "title": "Finish project documentation",
            "label": "Documentation",
            "description": "Complete the documentation for the project before the deadline.",
            "status": "backlog",
            "estimated_time": "01:30:00",
            "execution_time": "00:45:00",
            "importance": "high"
        }, 
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        })


        response = self.client.put("/1", 
        json = {
            "title": "Improve project documentation",
        }, 
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        })

        self.assertEqual(response.status_code, 200, "Task update failed with existing task")


    def test_failed_update_task(self):
        """ Test update task without existing task """

        response = self.client.put("/1", 
        json = {
            "title": "Improve project documentation",
        }, 
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        })

        self.assertEqual(response.status_code, 404, "Task update suceded without existing task")


    def test_successful_delete_task(self):
        """ Test delete task with existing task """

        self.client.post("",
        json = {
            "title": "Finish project documentation",
            "label": "Documentation",
            "description": "Complete the documentation for the project before the deadline.",
            "status": "backlog",
            "estimated_time": "01:30:00",
            "execution_time": "00:45:00",
            "importance": "high"
        }, 
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        })


        response = self.client.delete("/1", headers = {
            "Authorization": f"Bearer {self.access_token}"
        })

        self.assertEqual(response.status_code, 204, "Task delete failed with existing task")


    def test_failed_delete_task(self):
        """ Test delete task without existing task """

        response = self.client.delete("/1", headers = {
            "Authorization": f"Bearer {self.access_token}"
        })

        self.assertEqual(response.status_code, 404, "Task delete suceded without existing task")