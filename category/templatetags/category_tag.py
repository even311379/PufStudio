from django import template
from ..models import Category
from blog.models import MajorCategory

register = template.Library()


@register.simple_tag()
def get_children_categories(parent_name):
    CAT = Category.objects.filter(name=parent_name).first()
    if CAT:
        return CAT.get_children()
    else:
        return []


@register.simple_tag()
def get_major_categories():
    return MajorCategory.objects.all().order_by('sort_order')
