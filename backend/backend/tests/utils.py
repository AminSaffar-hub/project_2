from django.contrib.auth.models import User

from backend.models import Category, Item, Shop


class TestCaseWithDataMixin:
    def setUp(self):
        super().setUp()

        self.clothes = Category.objects.create(name="clothes")
        self.self_care = Category.objects.create(name="self-care")
        self.appliances = Category.objects.create(name="appliances")
        self.food = Category.objects.create(name="food")
        self.other = Category.objects.create(name="other")

        self.shop1 = Shop.objects.create(name="disney")
        self.shop2 = Shop.objects.create(name="zalando")
        self.shop3 = Shop.objects.create(name="magic")

        self.item1 = Item.objects.create(
            title="shoe",
            price=150,
            discounted_price=100,
            link_to_post="http://url/to/shoe",
            link_to_image="http://url/to/shoe.png",
            description="best shoe in the world",
            category=self.clothes,
            provider=self.shop1,
        )

        self.item2 = Item.objects.create(
            title="panini machine",
            price=20,
            discounted_price=10,
            link_to_post="http://url/to/panini_machine",
            link_to_image="http://url/to/panini_machine.png",
            description="best panini machine in the world",
            category=self.appliances,
            provider=self.shop1,
        )

        # Create 10 test items
        for i in range(10):
            Item.objects.create(
                title=f"Item {i+1}",
                price=i + 1 * 5,
                discounted_price=i + 1 * 4,
                link_to_post=f"http://url/to/Item {i+1}",
                link_to_image=f"http://url/to/Item {i+1}.png",
                description=f"best Item {i+1} machine in the world",
                category=self.other,
                provider=self.shop2,
            )

        self.username = "Testuser"
        self.password = "testpassword"
        self.email = "testuse@example.com"
        self.first_name = "test"
        self.last_name = "user"
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
        )
