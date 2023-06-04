from backend.models import Article


class TestCaseWithDataMixin:
    def setUp(self):
        super().setUp()

        self.article1 = Article.objects.create(
            name="shoe",
            old_price="150",
            new_price="100",
            url="http://url/to/shoe",
            image_link="http://url/to/shoe.png",
            description="best shoe in the world",
            type=Article.ProductType.CLOTHES,
        )

        self.article2 = Article.objects.create(
            name="makeup",
            old_price="20",
            new_price="10",
            url="http://url/to/makeup",
            image_link="http://url/to/makeup.png",
            description="best makeup in the world",
            type=Article.ProductType.SELF_CARE,
        )

        self.article2 = Article.objects.create(
            name="panini machine",
            old_price="20",
            new_price="10",
            url="http://url/to/panini_machine",
            image_link="http://url/to/panini_machine.png",
            description="best panini machine in the world",
            type=Article.ProductType.APPLIANCES,
        )

        # Create 10 test articles
        for i in range(10):
            Article.objects.create(name=f"Article {i+1}")
