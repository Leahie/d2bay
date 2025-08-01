from users.models import CustomUser
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

# Create your tests here.

class CustomUserTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass'))

    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser')
