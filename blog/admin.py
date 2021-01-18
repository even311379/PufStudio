from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)

from wagtailorderable.modeladmin.mixins import OrderableMixin

from .models import PostSeries, MajorCategory, ExternalImage


class PostSeriesAdmin(OrderableMixin, ModelAdmin):
    model = PostSeries
    menu_label = 'Post Series'
    menu_icon = "fa-object-group"
    ordering = ['sort_order']
    list_display = ('name', 'slug')


class MajorCategoryAdmin(OrderableMixin, ModelAdmin):
    model = MajorCategory
    menu_label = 'Major Category'
    menu_icon = "fa-industry"
    ordering = ['sort_order']
    list_display = ('name', 'slug')


class ExternalImagesAdmin(ModelAdmin):
    model = ExternalImage
    menu_icon = 'fa-image'
    list_display = ('get_as_listing_header',)
    inspect_view_enabled = True
    inspect_view_fields = ('image_title', 'external_url')
    inspect_template_name = 'blog/external_image_inspect.html'


modeladmin_register(PostSeriesAdmin)
modeladmin_register(MajorCategoryAdmin)
modeladmin_register(ExternalImagesAdmin)
