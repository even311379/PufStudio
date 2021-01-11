from django import template
from home.models import HomePage
register = template.Library()


@register.simple_tag()
def is_english_page(page):
    return page.url.startswith('/en')