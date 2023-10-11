from modeltranslation.translator import TranslationOptions, translator
from backend.models import Category


class CategoryTranslationOptions(TranslationOptions):
    fields = ("name",)


translator.register(Category, CategoryTranslationOptions)
