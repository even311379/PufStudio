from django import template
from ..models import Category
from blog.models import MajorCategory
# from blog.models import Post

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.filter(name="Root").first().get_descendants()


@register.simple_tag()
def get_category_path(page, name):
    language = page.url.split('/')[1]
    return f'/{language}/?category={name}'

@register.simple_tag()
def get_major_categories():
    return MajorCategory.objects.all
