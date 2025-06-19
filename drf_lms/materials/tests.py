from rest_framework.test import APITestCase
from users.models import CustomUser
from materials.models import Course
from materials.models import Subscription

class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@example.com', password='testpass')
        self.course = Course.objects.create(title='Django', owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        response = self.client.post(f'/api/materials/courses/{self.course.id}/subscribe/')
        self.assertEqual(response.status_code, 201)

    def test_unsubscribe(self):
        sub = Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.delete(f'/api/materials/courses/{self.course.id}/unsubscribe/')
        self.assertEqual(response.status_code, 204)