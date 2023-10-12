from datetime import date
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
        (ValidationError, {'email': 'test02@example.com', 'username': "UserWithSameEmail"}),  # repeat email
        (ValidationError, {'email': 'test03@example.com', 'username': "User Вася"}),
    ]

    def setUp(self):
        self.site = AdminSite()

    def _create_user(self, **kwargs):
        user = None
        with transaction.atomic():
            user = CoreUser(**kwargs)
            user.set_password("dummy_password_#$@!*()")
            user.full_clean()
            user.save()
        return user

    def test_core_models(self):
        print("\n --- Testing core models")
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

        # test superuser
        ADMIN_EMAIL = "test_admin@example"
        CoreUser.objects.create_superuser(email=ADMIN_EMAIL, password="test_pass_9yAj")
        user = CoreUser.objects.get(email=ADMIN_EMAIL)
        print(f"superuser: {user.admin_display_name()}")

        # create clubs
        club = SportClub(name='Test club', location='Test, St. Petersburg')
        club.full_clean()
        club.save()

        # create profile

        kwargs_list = [
                {'first_name': "John", 'last_name': "Smith", "date_of_birth": date(1997, 1, 14)},
                {'first_name': "Ivan", 'last_name': "Smith", "date_of_birth": date(1968, 12, 14)},
                {'first_name': "Иван", 'middle_name': "Иванович",
                 'last_name': "Смит", "date_of_birth": date(1968, 5, 20)},
            ]
        for kwargs in kwargs_list:
            profile = Profile(**kwargs)
            profile.full_clean()
            profile.save()
            print(f"--\nprofile: {profile.get_full_name()} {profile.date_of_birth}")
            chancode = profile.make_chancode()
            print(f"profile id: {chancode.format()}"
                  f" decode: {chancode.decode_year_offset(chancode.encode()[-2:])}")
            self.assertTrue(chancode.validate(chancode.format()))
            print("chancode validated")

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
