from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import SystemUser, Announcement
from rest_framework_simplejwt.tokens import RefreshToken

def generate_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

class RegisterTestCase(APITestCase):
    def test_register_success(self):
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "123456789"
        }
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("username", response.data)

    def test_register_duplicate_email(self):
        SystemUser.objects.create_user(
            username="existinguser",
            email="testuser@example.com",
            password="password123"
        )
        data = {
            "username": "newuser",
            "email": "testuser@example.com",
            "password": "password123",
            "first_name": "New",
            "last_name": "User"
        }
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        
class LoginTestCase(APITestCase):
    def setUp(self):
        self.user = SystemUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )

    def test_login_success(self):
        data = {"username": "testuser", "password": "password123"}
        response = self.client.post("/api/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_login_invalid_credentials(self):
        data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post("/api/login/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        
class AnnouncementListTestCase(APITestCase):
    def setUp(self):
        self.user = SystemUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )
        Announcement.objects.create(
            subject="Math Tutoring",
            content="Learn math with me!",
            hourly_rate=50.00,
            author=self.user
        )

    def test_get_announcements(self):
        response = self.client.get("/api/announcements/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        
class AddAnnouncementTestCase(APITestCase):
    def setUp(self):
        self.user = SystemUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )
        self.token = generate_token(self.user)

    def test_add_announcement_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        data = {
            "subject": "Physics Tutoring",
            "content": "Learn physics with me!",
            "hourly_rate": 60.00
        }
        response = self.client.post("/api/announcements/add/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("subject", response.data)

    def test_add_announcement_unauthorized(self):
        data = {
            "subject": "Physics Tutoring",
            "content": "Learn physics with me!",
            "hourly_rate": 60.00
        }
        response = self.client.post("/api/announcements/add/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
class EditAnnouncementTestCase(APITestCase):
    def setUp(self):
        self.user = SystemUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )
        self.token = generate_token(self.user)
        self.announcement = Announcement.objects.create(
            subject="Math Tutoring",
            content="Learn math with me!",
            hourly_rate=50.00,
            author=self.user
        )

    def test_edit_announcement_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        data = {"subject": "Advanced Math Tutoring"}
        response = self.client.put(f"/api/announcements/edit/{self.announcement.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["subject"], "Advanced Math Tutoring")

    def test_edit_announcement_unauthorized(self):
        data = {"subject": "Advanced Math Tutoring"}
        response = self.client.put(f"/api/announcements/edit/{self.announcement.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
class DeleteAnnouncementTestCase(APITestCase):
    def setUp(self):
        self.user = SystemUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )
        self.token = generate_token(self.user)
        self.announcement = Announcement.objects.create(
            subject="Math Tutoring",
            content="Learn math with me!",
            hourly_rate=50.00,
            author=self.user
        )

    def test_delete_announcement_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.delete(f"/api/announcements/delete/{self.announcement.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_announcement_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.delete("/api/announcements/delete/999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)