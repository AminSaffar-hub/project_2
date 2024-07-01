import json

from django.core.management.base import BaseCommand

from backend.models import Category


class Command(BaseCommand):
    def find_category_score(self, category, category_scores):
        return [
            category_score["score"]
            for category_score in category_scores
            if category_score["category"] == category
        ][0]

    def find_category_translation(self, category, language, category_translations):
        return [
            category_translation[language]
            for category_translation in category_translations
            if category_translation["category"] == category
        ][0]

    def handle(self, *args, **options):
        try:
            Category.objects.all().delete()
            categories_json_path = (
                "/home/modamine/project_2/backend/backend/categorizer/categories.json"
            )

            possible_predictions = []
            with open(categories_json_path, "r") as f:
                categories = json.load(f)
                possible_predictions = categories["categories_relations"]
                translations = categories["categories_translations"]
                scores = categories["categories_scores"]

            main_categories = set(
                [prediction.get("main_category") for prediction in possible_predictions]
            )

            for category in main_categories:
                Category.objects.update_or_create(
                    name=category,
                    name_fr=self.find_category_translation(
                        category, "fr", translations
                    ),
                    score=self.find_category_score(category, scores),
                    parent=None,
                )
            sub_categories = []
            for prediction in possible_predictions:
                sub_categories.append(prediction.get("subcategory"))
                Category.objects.update_or_create(
                    name=prediction.get("subcategory"),
                    name_fr=self.find_category_translation(
                        category, "fr", translations
                    ),
                    score=self.find_category_score(category, scores),
                    parent=Category.objects.filter(
                        name=prediction.get("main_category")
                    ).first(),
                    category_predictor_id=prediction.get("category_predictor_id"),
                )

        except Exception as e:
            print(e)
