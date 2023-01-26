from pprint import pprint

from django.contrib.admin.sites import AdminSite
from django.core.exceptions import ValidationError
from django.db import transaction
from django.test import Client, TestCase

from core.admin import CoreUserAdmin, ProfileAdmin
from core.models import CoreUser, Profile, SportClub


class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self, perm, obj=None):
        return True


request = MockRequest()
request.user = MockSuperUser()


class CoreTestCase(TestCase):
    client = Client()
    VALID_USER_EMAIL = 'valid@example.com'

    TEST_CREDS = [
        (False, {'email': VALID_USER_EMAIL}),
        (ValidationError, {'email': 'test42@example.com', 'username': "User 42"}),
        (ValidationError, {'email': 'invalidmail'}),
        (False, {'email': 'test02@example.com', 'username': "User_42"}),
    ]

    def setUp(self):
        self.site = AdminSite()

    def _create_user(self, **kwargs):
        user = None
        with transaction.atomic():
            user = CoreUser.objects.create_user(**kwargs)
            user.full_clean()
        return user

    def test_core_models(self):
        print("\n --- Testing core users")
        user = None
        for exception_class, creds in self.TEST_CREDS:
            pprint(creds)
            if exception_class:
                print(f"Must fail with {exception_class.__name__}")
                with self.assertRaises(exception_class):
                    user = self._create_user(**creds)
            else:
                print("Must pass")
                user = self._create_user(**creds)
                print(f"id.{user.pk} '{user.username}' email='{user.email}'")

        count = CoreUser.objects.count()
        pprint(CoreUser.objects.all())
        self.assertEqual(count, len([1 for e, v in self.TEST_CREDS if e is False]))

        # create clubs
        club = SportClub(name='Test club', location='Test, St. Petersburg')
        club.full_clean()
        club.save()

        # create profile

        kwargs = {'first_name': "John", 'last_name': "Smith"}
        profile = Profile(**kwargs)
        profile.full_clean()
        profile.save()
        profile.club = club
        profile.owner = CoreUser.objects.get(email=self.VALID_USER_EMAIL)
        profile.full_clean()
        profile.save()

    def test_admin_core(self):
        print("\n --- Testing core admin")
        user_admin = CoreUserAdmin(model=CoreUser, admin_site=self.site)
        profile_admin = ProfileAdmin(model=Profile, admin_site=self.site)
        print(profile_admin)  # TODO REMOVE

        form_class = user_admin.get_form(request=request)
        print(f"user form_class: {form_class.__name__}")
        for exception_class, creds in self.TEST_CREDS:
            creds_with_pwd = creds.copy()
            creds_with_pwd.update({'password1': "xot4-bon89", 'password2': "xot4-bon89"})
            form = form_class(data=creds_with_pwd)
            valid = form.is_valid()
            print(form.instance.username)
            pprint(creds_with_pwd)
            if not valid:
                print("- form is invalid:")
                pprint(form.errors.as_data())
            else:
                print("- form valid")

            if exception_class:
                print("- must be invalid form")
                self.assertIs(valid, False)
            else:
                print("- must be valid form")
                self.assertIs(valid, True)
                form.save()
            # user_admin.save_model(obj=CoreUser(**creds), request=request, form=None, change=None)
