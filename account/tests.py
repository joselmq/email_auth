from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.urls import resolve, reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from account.permissions import IsSuperuser
from account.views import ListUsersView, SignUpView, UpdateUserView
from rest_framework.utils import json


class UpdateUserViewTest(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='username',
            password='password_1',
            first_name='jose')
        self.user.is_superuser = True
        self.user.save()
        self.user_not_superuser = User.objects.create_user(
            username='username2',
            password='password_1',
            first_name='jose')
        self.user_not_superuser.save()
        self.client = APIClient()

    def test_update_success(self):
        self.client.force_authenticate(self.user)
        new_first_name = 'new first name'
        new_last_name = 'new last name'
        response = self.client.put(
            reverse('update_user', kwargs={'pk': self.user.pk}),
            data={'first_name': new_first_name,
                  'last_name': new_last_name})
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.first_name, new_first_name)

    def test_update_fail(self):
        self.client.force_authenticate(self.user_not_superuser)
        new_last_name = 'new last name'
        response = self.client.put(
            reverse('update_user', kwargs={'pk': self.user.pk}),
            data={'last_name': new_last_name})
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)


class PermissionsTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='username',
            password='password_1',
            first_name='jose')
        self.user.is_superuser = True
        self.user.save()
        self.user_not_superuser = User.objects.create_user(
            username='username2',
            password='password_1',
            first_name='jose')
        self.user_not_superuser.save()
        self.client = APIClient()

    def test_is_superuser_fail(self):
        self.client.force_authenticate(self.user)

        request = RequestFactory()
        request.user = self.user

        request_2 = RequestFactory()
        request_2.user = self.user_not_superuser

        self.assertTrue(IsSuperuser().has_permission(request, ''))
        self.assertFalse(IsSuperuser().has_permission(request_2, ''))


class TestUrls(APITestCase):

    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='username',
            password='password_1',
            first_name='jose')
        self.user.is_superuser = True
        self.user.save()

    def test_list_users(self):
        url = reverse('list_users')
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(resolve(url).func.view_class, ListUsersView)
        self.assertEqual(User.objects.all().count(), len(response.data))
        self.assertEqual(response.data[0]['username'], 'username')

    def test_update_user(self):
        url = reverse('update_user', args=[str(self.user.pk)])
        self.assertEqual(resolve(url).func.view_class, UpdateUserView)

    def test_add_user(self):
        url = reverse('add_user')
        self.assertEqual(resolve(url).func.view_class, SignUpView)


class SignUpViewTest(APITestCase):
    def test_success(self):
        response = self.client.post(
            reverse('add_user'),
            data={'username': 'username_123',
                  'email': 'email@em.ail',
                  'password': 'password_1',
                  'first_name': 'José',
                  'last_name': 'Martínez'})
        self.assertEqual(response, status.HTTP_201_CREATED)
