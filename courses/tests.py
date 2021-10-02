from django.http import request
from django.shortcuts import get_object_or_404
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from courses.models import Course

# Create your tests here.

class CourseModelTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='user1', password = make_password('12341'), email='user1@example.com')
        course = Course.objects.create(name='Physics', maxquantity = '5', semester = '1', year = '1')

    def test_index_view_with_authentication(self):
        c = Client()
        user = User.objects.get(username='user1')
        c.force_login(user)
        response = c.get(reverse('courses:index'))
        self.assertEqual(response.status_code, 200)

    def test_courses_course(self):
        c = Client()
        c1 = Course.objects.first()
        c1.save()
        response = c.get(reverse('courses:course', args=(c1.id,)))
        self.assertEqual(response.status_code, 200)

    def test_book_without_authentication(self):
        c1 = Course.objects.first()
        c1.save()

        c = Client()
        response = c.get(reverse('courses:book', args=(c1.id,)))
        self.assertEqual(c1.students.count(), 0)

    def test_book_with_authentication(self):
        user = User.objects.get(username='user1')
        c1 = Course.objects.first()
        c1.save()

        c = Client()
        c.force_login(user)
        response = c.get(reverse('courses:book', args=(c1.id,)))
        self.assertEqual(c1.students.count(), 1)

    def test_remove_without_authentication(self):
        c1 = Course.objects.first()
        c1.save()

        c = Client()
        response = c.get(reverse('courses:remove', args=(c1.id,)))
        self.assertEqual(c1.students.count(), 0)

    def test_remove_with_authentication(self):
        user = User.objects.get(username='user1')
        c1 = Course.objects.first()
        c1.save()

        c = Client()
        c.force_login(user)
        response1 = c.get(reverse('courses:book', args=(c1.id,)))
        self.assertEqual(c1.students.count(), 1)
        response2 = c.get(reverse('courses:remove', args=(c1.id,)))
        self.assertEqual(c1.students.count(), 0)

    def test_godhand(self):
        user = User.objects.get(username='user1')
        user.is_superuser = True
        user.save()
        c1 = Course.objects.first()
        c1.save()
        c = Client()
        c.force_login(user)
        response1 = c.get(reverse('courses:godhand', args=(c1.id,)))
        c1.status = False
        c1.save()
        response2 = c.get(reverse('courses:godhand', args=(c1.id,)))