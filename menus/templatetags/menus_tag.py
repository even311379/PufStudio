from django import template

from ..models import Menu, MenuItem

register = template.Library()


@register.simple_tag()
def get_menu(slug):
    m = Menu.objects.filter(slug=slug).first()
    if m:
        print(m.menu_items.values())
        if len(m.menu_items.values()) == 1:
            return m.menu_items.first()
        return m 
    emptyItem = MenuItem(title_en='empty', title_zh='空的')
    return Menu(title='empty', menu_items=[emptyItem])