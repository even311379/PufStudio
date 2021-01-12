from django import template
from home.models import HomePage
register = template.Library()


@register.simple_tag()
def is_english_page(page):
    return page.url.startswith('/en')

@register.simple_tag()
def get_current_language_path(page):
    return page.url.split('/')[1]

@register.simple_tag()
def has_translation(page):
    if not hasattr(page, 'is_zh_finished'):
        return True
    if is_english_page(page):
        return page.is_zh_finished
    else:
        return page.is_en_finished

@register.simple_tag()
def get_other_url(request):
    full_url = request.build_absolute_uri()
    if '/en/' in full_url:
        return full_url.replace('/en/', '/zh-hant/')
    else:
        return full_url.replace('/zh-hant/', '/en/')

@register.simple_tag()
def get_other_language_text(page):
    if is_english_page(page):
        return '繁體中文'
    else:
        return 'english'