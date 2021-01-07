from .models import AppsPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

@register(AppsPage)
class AppsPageTR(TranslationOptions):
    fields = (
       'subtitle',
    )
