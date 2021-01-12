from django.db import models

from django import forms
from django.core.exceptions import PermissionDenied
from django.core.validators import MinLengthValidator, RegexValidator
from django.template.loader import render_to_string

from treebeard.mp_tree import MP_Node
from wagtail.admin.edit_handlers import FieldPanel


from wagtail.admin.forms import WagtailAdminModelForm
from wagtail.search import index

## copy nested category from
# https://www.codementor.io/@lb0/harnessing-the-power-of-django-and-python-to-build-a-configurable-taxonomy-gi88j23vl
# with only little modification

node_name_validator = RegexValidator(
    regex='^[\w][a-zA-Z &0-9]+$',
    message="Letters, numbers and '&' only plus must start with a letter.",
)

class Category(index.Indexed, MP_Node):
    title = models.CharField(max_length=30, unique=True, blank=True)
    name = models.CharField(max_length=50, unique=True, validators=[node_name_validator, MinLengthValidator(2)])
    node_order_index = models.IntegerField(blank=True, default=0, editable=False)
    sibling_order_index = models.IntegerField(blank=True, default=0, editable=True)
    node_child_verbose_name = 'child'
    node_order_by = ['node_order_index', 'sibling_order_index', 'name']

    panels = [
        FieldPanel('title'),
        FieldPanel('name'),
        FieldPanel('sibling_order_index')
    ]

    search_fields = [
        index.SearchField('title'),
        index.SearchField('name', partial_match=True)
    ]

    def get_as_listing_header(self):
        depth = self.get_depth()
        return render_to_string(
            'category/node_list_header.html',
            {
                'depth': depth,
                'depth_margin': (depth - 1)*5,
                'is_root': self.is_root(),
                'name': self.name,
                'title': self.title,
            }
        )

    get_as_listing_header.short_description = 'Name'
    get_as_listing_header.admin_order_field = 'name'

    def get_parent(self, *args, **kwargs):
        return super().get_parent(*args, **kwargs)

    get_parent.short_description = 'Parent'

    def delete(self):
        if self.is_root():
            raise PermissionDenied('Cannot delete root topic')
        else:
            super().delete()


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


# node form
class BasicNodeChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        depth_line = '-' * (obj.get_depth() - 1)
        return f"{depth_line} {super().label_from_instance(obj)}"


class NodeForm(WagtailAdminModelForm):
    parent = BasicNodeChoiceField(required=True, queryset=Category.objects.all(), empty_label=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs['instance']

        if instance.is_root() or Category.objects.count() == 0:
            self.fields['parent'].disabled = True
            self.fields['parent'].required = False
            self.fields['parent'].empty_label = 'N/A - Root Node'
            self.fields['parent'].widget = forms.HiddenInput()

            self.fields['name'].label += ' (Root)'
        elif instance.id:
            self.fields['parent'].initial = instance.get_parent()

    def save(self, commit=True, *args, **kwargs):
        instance = super().save(commit=False, *args, **kwargs)
        parent = self.cleaned_data['parent']

        if not commit:
            return instance
        if instance.id is None:
            if Category.objects.all().count() == 0:
                Category.add_root(instance=instance)
            else:
                instance = parent.add_child(instance=instance)
        else:
            instance.save()
            if instance.get_parent() != parent:
                instance.move(parent, pos='sorted-child')
        return instance


Category.base_form_class = NodeForm
