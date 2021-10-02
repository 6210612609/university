from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from courses.models import Course

# Create your tests here.

class UserViewTestCase(TestCase):

    def setUp(self):
        User.objects.create(username='user1', password = make_password('1234'), email='user@example.com')
        Course.objects.create(name='Physics', maxquantity = '5', semester = '1', year = '1')

    def test_index_view_with_authentication(self):
        c = Client()
        user = User.objects.get(username='user1')
        c1 = Course.objects.first()
        c1.save()
        c.force_login(user)
        response1 = c.get(reverse('courses:book', args=(c1.id,)))        
        response2 = c.get(reverse('users:index'))
        self.assertEqual(response2.status_code, 200)

    def test_index_view_without_authentication(self):
        c = Client()
        response = c.get(reverse('users:index'))
        self.assertEqual(response.status_code, 302)

    def test_login_view_successful(self):
        c = Client()
        user = User.objects.get(username='user1')
        
        c.force_login(user)
        response = c.post(reverse('users:login'), {'username': 'user1', 'password': '1234'})
        self.assertEqual(response.status_code, 302)
    
    def test_login_view_unsuccessful(self):
        c = Client()
        user = User.objects.get(username='user1')
        
        c.force_login(user)
        response = c.post(reverse('users:login'), {'username': '', 'password': '1234'})
        self.assertEqual(response.status_code, 200)
    
    def test_login_view_with_authentication(self):
        c = Client()
        user = User.objects.get(username='user1')
        
        c.force_login(user)
        response = c.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_without_authentication(self):
        c = Client()
        response = c.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view_without_authentication(self):
        c = Client()
        response = c.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 200)
    

    