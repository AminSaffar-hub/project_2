from backend.models import Item
from django.contrib.auth.models import User


class TestCaseWithDataMixin:
    def setUp(self):
        super().setUp()

        self.item1 = Item.objects.create(
            title="shoe",
            price=150,
            discounted_price=100,
            link_to_post="http://url/to/shoe",
            link_to_image="http://url/to/shoe.png",
            description="best shoe in the world",
            category=Item.ItemCategories.CLOTHES,
        )

        self.item2 = Item.objects.create(
            title="makeup",
            price=20,
            discounted_price=10,
            link_to_post="http://url/to/makeup",
            link_to_image="http://url/to/makeup.png",
            description="best makeup in the world",
            category=Item.ItemCategories.SELF_CARE,
        )

        self.item2 = Item.objects.create(
            title="panini machine",
            price=20,
            discounted_price=10,
            link_to_post="http://url/to/panini_machine",
            link_to_image="http://url/to/panini_machine.png",
            description="best panini machine in the world",
            category=Item.ItemCategories.APPLIANCES,
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
                category=Item.ItemCategories.OTHER,
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
