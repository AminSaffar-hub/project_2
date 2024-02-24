from django.conf import settings
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.core.paginator import EmptyPage
from frontend.views import home

from backend.models import Item, Like
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
        self.assertContains(response, "shoe")
        self.assertContains(response, "panini machine")
        self.assertContains(response, "Item 2")
        self.assertContains(response, "Item 3")

    def test_home_view_pagination(self):
        request = self.factory.get("/", {"page": 2})
        response = home(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Item 9")
        self.assertNotContains(response, "Item 3")
        self.assertNotContains(response, "Item 2")

    def test_home_view_with_search(self):
        request = self.factory.get("/", {"search": "shoe"})
        response = home(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "shoe")
        self.assertNotContains(response, "makeup")
        self.assertNotContains(response, "panini machine")

    def test_pagination_on_searched_items(self):
        request = self.factory.get("/", {"page": 2, "search": "Item"})
        response = home(request)

        self.assertNotContains(response, "Item 3")
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

    def test_products_catgeories(self):
        item1 = Item.objects.create(
            title="Item 1",
            price=10,
            discounted_price=8,
            category=self.food,
        )
        item2 = Item.objects.create(
            title="Item 2",
            price=15,
            discounted_price=10,
            category=self.food,
        )
        item3 = Item.objects.create(title="Item 3", category=self.clothes)
        item4 = Item.objects.create(title="Item 3", category=self.self_care)
        request = self.factory.get("/", {"category": self.food})
        response = home(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, item1.title)
        self.assertContains(response, item2.title)
        self.assertNotContains(response, item3.title)
        self.assertNotContains(response, item4.title)

    def test_get_shop(self):
        response = self.client.get(f"/?shop={self.shop1.name}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item1.title)
        self.assertContains(response, self.item2.title)

    def test_like_item(self):
        self.client.login(username="Testuser", password="testpassword")

        url = reverse("rate", args=[str(self.item1.id)])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["like"], True)

        self.assertTrue(Like.objects.filter(item=self.item1, user=self.user).exists())

        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["like"], False)

        self.assertFalse(Like.objects.filter(item=self.item1, user=self.user).exists())


class InternationalizationTestCase(TestCaseWithDataMixin, TestCase):
    def test_fr_translation(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "fr"})
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Connexion")

    def test_en_translation(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en"})
        response = self.client.get(reverse("home"))
        self.assertContains(response, "login")


class ErrorViewsTest(TestCaseWithDataMixin, TestCase):
    def test_404_handler(self):
        response = self.client.get(reverse("product_details", kwargs={"pk": 7846000}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "frontend/404.html")

    def test_500_handler(self):
        with self.assertRaises(EmptyPage):
            response = self.client.get("/?page=500")
            self.assertEqual(response.status_code, 500)
            self.assertTemplateUsed(
                response, "frontend/404.html"
            )  # Assuming this is correct, update as needed
