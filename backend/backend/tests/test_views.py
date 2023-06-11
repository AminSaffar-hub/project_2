from django.test import TestCase, RequestFactory

from backend.tests.utils import TestCaseWithDataMixin
from frontend.views import home


class ViewsTests(TestCaseWithDataMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()

    def test_home_view_without_search(self):
        request = self.factory.get("/")
        response = home(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Article 1")
        self.assertContains(response, "Article 2")
        self.assertContains(response, "Article 3")

    def test_home_view_with_search(self):
        request = self.factory.get("/", {"search": "shoe"})
        response = home(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "shoe")
        self.assertNotContains(response, "makeup")
        self.assertNotContains(response, "panini machine")

    def test_home_view_pagination(self):
        request = self.factory.get("/", {"page": 2})
        response = home(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Article 9")
        self.assertNotContains(response, "Article 1")
        self.assertNotContains(response, "Article 2")

    def test_pagination_on_searched_items(self):
        request = self.factory.get("/", {"page": 2, "search": "Article"})
        response = home(request)

        self.assertNotContains(response, "Article 1")
        self.assertNotContains(response, "Article 7")
        self.assertNotContains(response, "shoe")

    def test_product_description(self):
        response = self.client.get(f"/{self.article1.pk}")

        self.assertContains(response, self.article1.name)
        self.assertContains(response, self.article1.url)
        self.assertContains(response, self.article1.old_price)
        self.assertContains(response, self.article1.new_price)
        self.assertContains(response, self.article1.description)

        self.assertTemplateUsed(response, "frontend/product_details.html")
