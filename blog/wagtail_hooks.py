from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)

from wagtailorderable.modeladmin.mixins import OrderableMixin

from .models import VVV


class YourModelAdmin(OrderableMixin, ModelAdmin):
    model = VVV

    ordering = ['sort_order']

modeladmin_register(YourModelAdmin)