from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register, ModelAdminGroup)

from wagtailorderable.modeladmin.mixins import OrderableMixin

from .models import PostSeries, MajorCategory, ExternalImage, PostPage
from category.admin import CategoryAdmin

class PostSeriesAdmin(OrderableMixin, ModelAdmin):
    model = PostSeries
    menu_label = 'Post Series'
    menu_icon = "fa-object-group"
    ordering = ['sort_order']
    list_display = ('name', 'slug')


class MajorCategoryAdmin(OrderableMixin, ModelAdmin):
    model = MajorCategory
    menu_label = 'Major Category'
    menu_icon = "group"
    ordering = ['sort_order']
    list_display = ('name', 'slug')


class ExternalImagesAdmin(ModelAdmin):
    model = ExternalImage
    menu_icon = 'fa-image'
    list_display = ('get_as_listing_header',)
    inspect_view_enabled = True
    inspect_view_fields = ('image_title', 'external_url')
    inspect_template_name = 'blog/external_image_inspect.html'

class PostPageAdmin(ModelAdmin):
    model = PostPage
    menu_order = 200
    menu_icon = 'fa-comment'
    list_display = ('title', 'visits','series_id', )
    list_filter = ('is_en_finished', 'is_zh_finished', 'series_name', 'major_category', 'categories', )
    search_fields = ('title', 'subtitle',)

class Grouping(ModelAdminGroup):
    menu_label = 'ExtraGroup'
    menu_icon = 'fa-industry'
    menu_order = 300
    items = (PostSeriesAdmin,MajorCategoryAdmin, CategoryAdmin)

modeladmin_register(PostPageAdmin)
modeladmin_register(ExternalImagesAdmin)
modeladmin_register(Grouping)
