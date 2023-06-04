from django.test import TestCase, RequestFactory
from django.urls import reverse

from backend.tests.utils import TestCaseWithDataMixin
from frontend.views import home


class ViewsTests(TestCase, TestCaseWithDataMixin):
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()

    def test_home_view_without_search(self):
        # Create a GET request to the home view
        request = self.factory.get(reverse("home"))
        response = home(request)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "shoe")
        self.assertContains(response, "makeup")
        self.assertContains(response, "panini machine")

    def test_home_view_with_search(self):
        # Create a GET request with a search query to the home view
        request = self.factory.get(reverse("home", {"search": "shoe"}))
        response = home(request)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "shoe")
        self.assertNotContains(response, "makeup")
        self.assertNotContains(response, "panini machine")

    def test_home_view_pagination(self):
        # Create a GET request to the second page of the home view
        request = self.factory.get(reverse("home"), {"page": 2})
        response = home(request, page=2)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Article 9")
        self.assertContains(response, "Article 10")
        self.assertNotContains(response, "shoe")
        self.assertNotContains(response, "makeup")
