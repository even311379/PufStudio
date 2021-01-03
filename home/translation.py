from .models import HomePage, PageFolder
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

@register(HomePage)
class HomePageTR(TranslationOptions):
    fields = ()

@register(PageFolder)
class PageFolderTR(TranslationOptions):
    fields = ()
    