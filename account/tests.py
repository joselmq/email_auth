from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class UpdateUserViewTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='username', password='password_1', first_name='jose')
        self.client = APIClient()

    def test_success(self):
        new_first_name = 'new first name'
        new_last_name = 'new last name'
        print("self.user.pk")
        print(self.user.pk)
        response = self.client.put(
            reverse('update_user', kwargs={'pk': self.user.pk}),
            data={"first_name": new_first_name,
                  "last_name": new_last_name})
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.first_name, new_first_name)


class PermissionsTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create()

    # def test_is_superuser(self):
    #     IsSuperUser()
    #     self.assertRaises()
