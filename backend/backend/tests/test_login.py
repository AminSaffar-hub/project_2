from django.test import TestCase
from django.urls import reverse

from backend.tests.utils import TestCaseWithDataMixin


class LoginViewsTests(TestCaseWithDataMixin, TestCase):
    def test_user_login(self):
        login_url = reverse("login")
        data = {"username": self.username, "password": self.password}
        response = self.client.post(login_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertRedirects(
            response, "/"
        )  # Ensure the redirection is to the home page

    def test_redirect_authenticated_user(self):
        self.client.login(username=self.username, password=self.password)
        login_url = reverse("login")
        response = self.client.get(login_url)
        self.assertRedirects(
            response, "/"
        )  # If user is authenticated, should redirect to home page

    def test_user_logout(self):
        self.client.login(username=self.username, password=self.password)
        logout_url = reverse("logout")
        response = self.client.get(logout_url)
        self.assertEqual(response.status_code, 302)  # Redirect to home after logout
        self.assertRedirects(
            response, "/"
        )  # Ensure the redirection is to the home page

    def test_profile_view(self):
        self.client.login(username=self.username, password=self.password)
        profile_url = reverse("profile")
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.username)
        self.assertContains(response, self.first_name)
        self.assertContains(response, self.last_name)
        self.assertContains(response, self.email)

    def test_edit_profile_view(self):
        self.client.login(username=self.username, password=self.password)
        edit_profile_url = reverse("edit_profile")
        data = {
            "first_name": "New",
            "last_name": "Name",
            # Add other fields for your EditProfileForm here
        }
        response = self.client.post(edit_profile_url, data)
        self.assertEqual(response.status_code, 200)
        # TODO: add this message:
        # self.assertContains(response, "Changed Profile: successful!")
        # Verify that the user's profile information has been updated in the database
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "New")
        self.assertEqual(self.user.last_name, "Name")

    def test_change_password_view(self):
        self.client.login(username=self.username, password=self.password)
        change_password_url = reverse("change_password")
        data = {
            "old_password": self.password,
            "new_password1": "newpassword123",
            "new_password2": "newpassword123",
        }
        response = self.client.post(change_password_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/profile.html")
        # TODO: add this message:
        # self.assertContains(response, "Changed Password: successful!")
        # Verify that the user's password has been updated in the database
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpassword123"))
