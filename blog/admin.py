from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)

from wagtailorderable.modeladmin.mixins import OrderableMixin

from .models import PostSeries, MajorCategory


class PostSeriesAdmin(OrderableMixin, ModelAdmin):
    model = PostSeries
    menu_label = 'Post Series'
    menu_icon = "fa-object-group"
    ordering = ['sort_order']
    list_display = ('name','slug')

class MajorCategoryAdmin(OrderableMixin, ModelAdmin):
    model = MajorCategory
    menu_label = 'Major Category'
    menu_icon = "fa-industry"
    ordering = ['sort_order']
    list_display = ('name','slug')

modeladmin_register(PostSeriesAdmin)
modeladmin_register(MajorCategoryAdmin)
