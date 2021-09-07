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
        self.user = User.objects.create_user(username='username', password='password_1', first_name='jose')
        self.user.is_superuser = True
        self.user.save()
        self.user_not_superuser = User.objects.create_user(username='username2',
                                                           password='password_1',
                                                           first_name='jose')
        self.user_not_superuser.save()
        self.client = APIClient()

    def test_update_success(self):
        self.client.login(username='username', password='password_1')
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
        self.client.login(username='username2', password='password_1')
        new_last_name = 'new last name'
        response = self.client.put(
            reverse('update_user', kwargs={'pk': self.user.pk}),
            data={'last_name': new_last_name})
        self.user.refresh_from_db()
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)


class PermissionsTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='username',
                                             password='password_1',
                                             first_name='jose')
        self.user.is_superuser = True
        self.user.save()
        self.user_not_superuser = User.objects.create_user(username='username2',
                                                           password='password_1',
                                                           first_name='jose')
        self.user_not_superuser.save()
        self.client = APIClient()

    def test_is_superuser_fail(self):
        self.client.login(username='username', password='password_1')
        # With URLS
        admin_pages = [
            "/admin/",
            "/admin/auth/",
            "/admin/auth/group/",
            "/admin/auth/group/add/",
            "/admin/auth/user/",
            "/admin/auth/user/add/",
            "/admin/password_change/"
        ]
        for page in admin_pages:
            response = self.client.get(page)
            self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        # With RequestFactory
        request = RequestFactory()
        request.user = self.user

        request_2 = RequestFactory()
        request_2.user = self.user_not_superuser

        self.assertTrue(IsSuperuser().has_permission(request, ''))
        self.assertFalse(IsSuperuser().has_permission(request_2, ''))


class TestUrls(APITestCase):

    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='username', password='password_1', first_name='jose')
        self.user.is_superuser = True
        self.user.save()
        self.client = APIClient()

    def test_list_users(self):
        url = reverse('list_users')
        self.assertEqual(resolve(url).func.view_class, ListUsersView)

        self.client.login(username='username', password='password_1')
        request = self.client.get('/users/')
        json_content = json.loads(request.content.decode('utf-8'))
        username = json_content[0]['username']
        self.assertEqual(username, 'username')

    def test_update_user(self):
        url = reverse('update_user', args=[str(self.user.pk)])
        self.assertEqual(resolve(url).func.view_class, UpdateUserView)

    def test_add_user(self):
        url = reverse('add_user')
        self.assertEqual(resolve(url).func.view_class, SignUpView)
