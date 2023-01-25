from pprint import pprint

from django.core.exceptions import ValidationError
from django.test import Client, TestCase

from core.models import CoreUser  # , Profile, SportClub


class CoreTestCase(TestCase):
    client = Client()

    """
    # def setUp(self):
        # Animal.objects.create(name="lion", sound="roar")
        # Animal.objects.create(name="cat", sound="meow")
    """

    def _create_user(self, **kwargs):
        user = CoreUser.objects.create_user(**kwargs)
        user.full_clean()
        return user

    def test_core_models(self):
        credentials = [
            (False, {'email': 'test@example.com'}),
            (ValidationError, {'email': 'test42@example.com', 'username': "User 42"}),
            (ValidationError, {'email': 'invalidmail'}),
            (False, {'email': 'test02@example.com', 'username': "User_42"}),
        ]

        print("Testing core users")
        for exception_class, creds in credentials:
            pprint(creds)
            if exception_class:
                print(f"Must fail with {exception_class.__name__}")
                with self.assertRaises(exception_class):
                    user = self._create_user(**creds)
            else:
                print("Must pass")
                user = self._create_user(**creds)
                print(f"id.{user.pk} '{user.username}' email='{user.email}'")
