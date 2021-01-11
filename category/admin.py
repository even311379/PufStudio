from django.shortcuts import get_object_or_404
from django.contrib.admin.utils import quote, unquote
from django.conf.urls import url
from wagtail.contrib.modeladmin.helpers import ButtonHelper
from wagtail.contrib.modeladmin.views import CreateView
from wagtail.contrib.modeladmin.options import ModelAdmin

from .models import Category
# Register your models here.


class NodeButtonHelper(ButtonHelper):
    """Custom button functionality for node listing buttons."""

    def prepare_classnames(self, start=None, add=None, exclude=None):
        """Parse classname sets into final css class list."""
        classnames = start or []
        classnames.extend(add or [])
        return self.finalise_classname(classnames, exclude or [])

    def delete_button(self, pk, *args, **kwargs):
        """Ensure that the delete button is not shown for root node."""
        instance = self.model.objects.get(pk=pk)
        if instance.is_root():
            return
        return super().delete_button(pk, *args, **kwargs)

    def inspect_button(self, *args, **kwargs):
        """Replace the term 'Inspect' with 'Details' in listing buttons."""
        button = super().inspect_button(*args, **kwargs)
        button['label'] = button['label'].replace('Inspect', 'Details')
        button['title'] = button['label'].replace('Inspect', 'Details', 1)
        return button

    def add_child_button(self, pk, child_verbose_name, **kwargs):
        """Build a add child button, to easily add a child under node."""
        classnames = self.prepare_classnames(
            start=self.edit_button_classnames + ['icon', 'icon-plus'],
            add=kwargs.get('classnames_add'),
            exclude=kwargs.get('classnames_exclude')
        )
        return {
            'classname': classnames,
            'label': 'Add %s %s' % (
                child_verbose_name, self.verbose_name),
            'title': 'Add %s %s under this one' % (
                child_verbose_name, self.verbose_name),
            'url': self.url_helper.get_action_url('add_child', quote(pk)),
        }

    def get_buttons_for_obj(self, obj, exclude=None, *args, **kwargs):
        """Override the getting of buttons, prepending create child button."""
        buttons = super().get_buttons_for_obj(obj, *args, **kwargs)

        add_child_button = self.add_child_button(
            pk=getattr(obj, self.opts.pk.attname),
            child_verbose_name=getattr(obj, 'node_child_verbose_name'),
            **kwargs
        )
        buttons.append(add_child_button)

        return buttons


class AddChildNodeViewClass(CreateView):
    """View class that can take an additional URL param for parent id."""

    parent_pk = None
    parent_instance = None

    def __init__(self, model_admin, parent_pk):
        self.parent_pk = unquote(parent_pk)
        object_qs = model_admin.model._default_manager.get_queryset()
        object_qs = object_qs.filter(pk=self.parent_pk)
        self.parent_instance = get_object_or_404(object_qs)
        super().__init__(model_admin)

    def get_page_title(self):
        """Generate a title that explains you are adding a child."""
        title = super().get_page_title()
        return title + ' %s %s for %s' % (
            self.model.node_child_verbose_name,
            self.opts.verbose_name,
            self.parent_instance
        )

    def get_initial(self):
        """Set the selected parent field to the parent_pk."""
        return {'parent': self.parent_pk}


class CategoryAdmin(ModelAdmin):
    model = Category
    menu_icon = 'fa-cube'
    menu_order = 800

    list_per_page = 50
    list_display = ('get_as_listing_header', 'get_parent')
    search_fields = ('name',)
    inspect_view_enabled = True
    inspect_view_fields = ('name', 'get_parent', 'id',)

    # other overrides
    button_helper_class = NodeButtonHelper

    def add_child_view(self, request, instance_pk):
        """Generate a class-based view to provide 'add child' functionality."""
        # instance_pk will become the default selected parent_pk
        kwargs = {'model_admin': self, 'parent_pk': instance_pk}
        view_class = AddChildNodeViewClass
        return view_class.as_view(**kwargs)(request)

    def get_admin_urls_for_registration(self):
        """Add the new url for add child page to the registered URLs."""
        urls = super().get_admin_urls_for_registration()
        add_child_url = url(
            self.url_helper.get_action_url_pattern('add_child'),
            self.add_child_view,
            name=self.url_helper.get_action_url_name('add_child')
        )
        return urls + (add_child_url, )
