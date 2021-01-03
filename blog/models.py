from django.db import models
from django import forms
from django.shortcuts import render

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtailcodeblock.blocks import CodeBlock
# from blog.blocks import CodeBlock

from wagtail.snippets.models import register_snippet
from taggit.models import TaggedItemBase, Tag
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.tags import ClusterTaggableManager

import datetime
from home.models import PageFolder

@register_snippet
class PostCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug')
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    
@register_snippet
class PostSeries(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug')
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "SeriesName"
        verbose_name_plural = "SeriesNames"


class PostTag(TaggedItemBase):
    content_object = ParentalKey(
        'PostPage',
        related_name = 'tagged_items',
        on_delete=models.CASCADE,
    )


class PostPage(Page):
    date = models.DateField("Post date", default=datetime.datetime.today)    
    thumbnail = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', blank=True, null=True)
    is_series = models.BooleanField(default='false')
    series_name = models.ForeignKey(PostSeries, on_delete=models.SET_NULL, related_name='+', blank=True, null=True)
    series_id = models.IntegerField(default=0, blank=True, null=True)

    subtitle = models.CharField(max_length=255, blank=True, null=True)
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('code', CodeBlock()),
        ('video', blocks.URLBlock()),
        ('image', ImageChooserBlock()),
    ])
    categories = ParentalManyToManyField('blog.PostCategory', blank = True)
    tags = ClusterTaggableManager(through='PostTag', blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle',classname="title"),
        StreamFieldPanel('body'),
        MultiFieldPanel([
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),        
            FieldPanel('tags')],
            heading='Group',
            classname='collapsible collapsed'
        )
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('date'),
        ImageChooserPanel('thumbnail'),
        MultiFieldPanel([
            FieldPanel('is_series'),
            FieldPanel('series_name'),
            FieldPanel('series_id')]),
    ]

class SearchResultPage(Page):

    def serve(self, request):
        if request.method == 'GET':
            # categories = request.GET.get('cats', None)
            # tags = request.GET.get('tags', None)
            # AllPosts = PostPage.objects.filter()

            # need some test 
            for post in PostPage.objects.live().descendant_of(PageFolder):        
                print(post.tags)
        render_data = locals()
        return render(request, 'blog/search_result_page.html', render_data)


