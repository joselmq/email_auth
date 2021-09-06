from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse
from rest_framework import status
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient, APITestCase

from account.views import ListUsersView, SignUpView, UpdateUserView


class UpdateUserViewTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='username', password='password_1', first_name='jose')
        self.client = APIClient()

    def test_update_success(self):
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
        new_last_name = 'new last name'
        response = self.client.put(
            reverse('update_user', kwargs={'pk': self.user.pk}),
            data={'last_name': new_last_name})
        self.user.refresh_from_db()
        self.assertRaisesMessage(HTTP_400_BAD_REQUEST, response)


class PermissionsTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='username', password='password_1', first_name='jose')
        self.client = APIClient()

    def test_is_superuser_fail(self):
        self.client.login(username='username', password='password_1')
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


class TestUrls(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='username', password='password_1', first_name='jose')
        self.client = APIClient()

    def test_list_users(self):
        url = reverse('list_users')
        self.assertEqual(resolve(url).func.view_class, ListUsersView)

    def test_update_user(self):
        url = reverse('update_user', args=[str(self.user.pk)])
        self.assertEqual(resolve(url).func.view_class, UpdateUserView)

    def test_add_user(self):
        url = reverse('add_user')
        self.assertEqual(resolve(url).func.view_class, SignUpView)
