from .models import Category
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(Category)
class CategoryTR(TranslationOptions):
    fields = (
        'title',
    )
