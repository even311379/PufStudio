from django.db import models
from django.shortcuts import render

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail_color_panel.fields import ColorField
from wagtail_color_panel.edit_handlers import NativeColorPanel
import datetime

# Create your models here.


class AppsPage(Page):
    date = models.DateField('Post Date', default=datetime.datetime.today)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    hero_color = ColorField(default="#ff0032")
    custom_html = models.TextField(blank=True, null=True)
    custom_python = models.TextField(blank=True, null=True)
    html_file = models.ForeignKey(
        'wagtaildocs.Document', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    brython_file = models.ForeignKey(
        'wagtaildocs.Document', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        NativeColorPanel('hero_color'),
        FieldPanel('custom_html'),
        FieldPanel('custom_python'),
        DocumentChooserPanel('html_file'),
        DocumentChooserPanel('brython_file')
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('date')
    ]
    parent_page_types = ['home.PageFolder']
    def serve(self, request):
        if (self.html_file):
            with self.html_file.file.open('r') as f:
                html_content = f.read()
        if (self.brython_file):
            with self.brython_file.file.open('r') as f:
                brython_content = f.read()
        render_data = locals()
        render_data['page'] = self
        return render(request, 'apps/apps_page.html', render_data) 