from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)

from wagtailorderable.modeladmin.mixins import OrderableMixin

from .models import PostSeries, MajorCategory, ExternalImage, PostPage


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

class PostPageAdmin(ModelAdmin):
    model = PostPage
    menu_icon = 'fa-comment'
    list_display = ('title',)
    list_filter = ('series_name', 'major_category', 'categories',)
    search_fields = ('title', 'subtitle',)


modeladmin_register(PostPageAdmin)
modeladmin_register(PostSeriesAdmin)
modeladmin_register(MajorCategoryAdmin)
modeladmin_register(ExternalImagesAdmin)
