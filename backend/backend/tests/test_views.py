from django.test import TestCase, RequestFactory

from backend.tests.utils import TestCaseWithDataMixin
from backend.models import Item
from frontend.views import home, NUMBER_OF_ITEMS_IN_PAGE


class ViewsTests(TestCaseWithDataMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()

    def test_home_view_without_search(self):
        request = self.factory.get("/")
        response = home(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Item 1")
        self.assertContains(response, "Item 2")
        self.assertContains(response, "Item 3")

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
        self.assertContains(response, "Item 9")
        self.assertNotContains(response, "Item 1")
        self.assertNotContains(response, "Item 2")

    def test_pagination_on_searched_items(self):
        request = self.factory.get("/", {"page": 2, "search": "Item"})
        response = home(request)

        self.assertNotContains(response, "Item 1")
        self.assertNotContains(response, "Item 7")
        self.assertNotContains(response, "shoe")

    def test_product_description(self):
        response = self.client.get(f"/{self.item1.pk}")

        self.assertContains(response, self.item1.title)
        self.assertContains(response, self.item1.link_to_post)
        self.assertContains(response, self.item1.price)
        self.assertContains(response, self.item1.discounted_price)
        self.assertContains(response, self.item1.description)

        self.assertTemplateUsed(response, "frontend/item_details.html")

    def test_top_promos_page(self):
        response = self.client.get("/top-promos")
        ordered_items = sorted(
            Item.objects.all(), key=lambda t: t.sale_percentage, reverse=True
        )[:NUMBER_OF_ITEMS_IN_PAGE]

        self.assertTemplateUsed(response, "frontend/home.html")
        self.assertEqual(list(response.context["items"]), ordered_items)
        self.assertEqual(response.context["items"].number, 1)
