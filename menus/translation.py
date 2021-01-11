from .models import Menu, MenuItem
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

@register(Menu)
class MenuTR(TranslationOptions):
    fields = (
        'title',
    )

@register(MenuItem)
class MenuItemTR(TranslationOptions):
    fields = (
        'title',
    )
