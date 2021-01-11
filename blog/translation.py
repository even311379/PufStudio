from .models import PostPage, SearchResultPage, PostSeries, MajorCategory, CategorySearchPage
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

@register(CategorySearchPage)
class CategorySearchTR(TranslationOptions):
    fields = (

    )

@register(PostSeries)
class PostSeriesTR(TranslationOptions):
    fields = (
        'name',
    )

@register(MajorCategory)
class MajorCategoryTR(TranslationOptions):
    fields = (
        'name',
    )
