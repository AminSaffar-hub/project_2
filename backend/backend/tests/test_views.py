from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.conf import settings

from frontend.views import NUMBER_OF_ITEMS_IN_PAGE, home
from backend.models import Item
from backend.tests.utils import TestCaseWithDataMixin


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

    def test_products_catgeories(self):
        item1 = Item.objects.create(title="Item 1", category=Item.ItemCategories.FOOD)
        item2 = Item.objects.create(title="Item 2", category=Item.ItemCategories.FOOD)
        item3 = Item.objects.create(
            title="Item 3", category=Item.ItemCategories.CLOTHES
        )
        item4 = Item.objects.create(
            title="Item 3", category=Item.ItemCategories.SELF_CARE
        )
        request = self.factory.get("/", {"category": Item.ItemCategories.FOOD})
        response = home(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, item1.title)
        self.assertContains(response, item2.title)
        self.assertNotContains(response, item3.title)
        self.assertNotContains(response, item4.title)


class InternationalizationTestCase(TestCaseWithDataMixin, TestCase):
    def test_fr_translation(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "fr"})
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Bon plans")
        self.assertContains(response, "Tous les promos")

    def test_en_translation(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en"})
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Top promos")
        self.assertContains(response, "All promos")
