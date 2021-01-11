from django import template

from ..models import Menu, MenuItem

register = template.Library()


@register.simple_tag()
def get_menu(slug, is_single=False):
    m = Menu.objects.filter(slug=slug).first()
    if m:
        if is_single == 1:
            return m.menu_items.first()
        return m
    return MenuItem(title=f'empty: {slug}')
