from .models import PostPage, SearchResultPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

@register(PostPage)
class PostPageTR(TranslationOptions):
    fields = (
       'subtitle',
       'body',
    )

@register(SearchResultPage)
class SearchResultTR(TranslationOptions):
    fields = ()