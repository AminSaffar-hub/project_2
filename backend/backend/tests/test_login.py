import re
from unittest.mock import patch

from captcha.client import RecaptchaResponse
from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from freezegun import freeze_time

from backend.tests.utils import TestCaseWithDataMixin


class LoginViewsTests(TestCaseWithDataMixin, TestCase):
    def test_user_login(self):
        login_url = reverse("login")
        data = {"username": self.username, "password": self.password}
        response = self.client.post(login_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertRedirects(response, "/")

    def test_redirect_authenticated_user(self):
        self.client.login(username=self.username, password=self.password)
        login_url = reverse("login")
        response = self.client.get(login_url)
        self.assertRedirects(response, "/")

    def test_user_logout(self):
        self.client.login(username=self.username, password=self.password)
        logout_url = reverse("logout")
        response = self.client.get(logout_url)
        self.assertEqual(response.status_code, 302)  # Redirect to home after logout
        self.assertRedirects(response, "/")

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
        }
        response = self.client.post(edit_profile_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Votre profile a été modifier avec succès.")

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
        self.assertContains(response, "Votre mot de passe a été modifier avec succés.")
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpassword123"))

    @patch("captcha.fields.client.submit")
    def test_valid_registration(self, mocked_submit):
        registration_url = reverse("register")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "newpassword123",
            "password2": "newpassword123",
            "g-recaptcha-response": "mock_recaptcha_response",
        }

        mocked_submit.return_value = RecaptchaResponse(is_valid=True)
        response = self.client.post(registration_url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")
        self.assertTrue(User.objects.filter(username="newuser").exists())

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_reset_password_view(self):
        reset_password_url = reverse("password_reset")
        response = self.client.get(reset_password_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ["login/resetpassword.html"])

        response = self.client.post(reset_password_url, {"email": self.email})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("password_reset_done"))

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("password reset on testserver", mail.outbox[0].subject.lower())
        self.assertIn(
            "Your username, in case you've forgotten: Testuser", mail.outbox[0].body
        )
        matches = re.search(r"/reset_password/.*/[a-zA-Z0-9\-]+/", mail.outbox[0].body)
        reset_password_reset_link = matches.group(0)
        response = self.client.get(reset_password_reset_link)
        self.assertEqual(response.status_code, 302)
        reset_password_form_link = response.url
        response = self.client.get(reset_password_form_link)
        self.assertEqual(response.status_code, 200)

        reset_data = {
            "new_password1": "verylongpass1234",
            "new_password2": "verylongpass1234",
        }
        response = self.client.post(reset_password_form_link, reset_data)
        self.assertEqual(response.status_code, 302)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("verylongpass1234"))

        response = self.client.get(reset_password_reset_link)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "The password reset link is invalid, possibly because it has been used."
            " Please request a new password reset.",
        )

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_reset_password_view_after_1_day(self):
        with freeze_time("2023-07-19 12:00:00"):
            reset_password_url = reverse("password_reset")
            self.client.post(reset_password_url, {"email": self.email})

        with freeze_time("2023-07-19 14:00:01"):
            matches = re.search(
                r"/reset_password/.*/[a-zA-Z0-9\-]+/", mail.outbox[0].body
            )
            reset_password_reset_link = matches.group(0)
            response = self.client.get(reset_password_reset_link)
            self.assertEqual(response.status_code, 200)
            self.assertContains(
                response,
                "The password reset link is invalid, possibly because it has been used."
                " Please request a new password reset.",
            )
