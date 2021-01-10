import random

from django.db import models
from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, FieldRowPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtailcodeblock.blocks import CodeBlock

from wagtail.snippets.models import register_snippet
from taggit.models import TaggedItemBase, Tag
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.tags import ClusterTaggableManager

import datetime


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
        related_name='tagged_items',
        on_delete=models.CASCADE,
    )


class PostPage(Page):
    date = models.DateField("Post date", default=datetime.datetime.today)
    thumbnail = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', blank=True, null=True)
    is_en_finished = models.BooleanField(default=False, blank=True, verbose_name='English Version Finished?')
    is_zh_finished = models.BooleanField(default=False, blank=True, verbose_name='Chinese Version Finished?')
    is_series = models.BooleanField(default=False)
    series_name = models.ForeignKey(
        PostSeries, on_delete=models.SET_NULL, related_name='+', blank=True, null=True)
    series_id = models.IntegerField(default=0, blank=True, null=True)

    subtitle = models.CharField(max_length=255, blank=True, null=True)
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title", icon='pick')),
        ('paragraph', blocks.RichTextBlock(icon='doc-full')),
        ('mermaid', blocks.TextBlock(icon='link')),
        ('code', CodeBlock(icon='code')),
        ('html', blocks.TextBlock(icon='plus-inverse')),
        ('video', blocks.URLBlock(icon='media')),
        ('image', ImageChooserBlock(icon='image')),
    ])
    categories = ParentalManyToManyField('blog.PostCategory', blank=True)
    tags = ClusterTaggableManager(through='PostTag', blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle', classname="full"),
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
        FieldRowPanel([
            FieldPanel('is_en_finished'),
            FieldPanel('is_zh_finished')],
            heading='Translation Finished?',
        ),
        ImageChooserPanel('thumbnail'),
        MultiFieldPanel([
            FieldPanel('is_series'),
            FieldPanel('series_name'),
            FieldPanel('series_id')],
            heading='Series Setting',
            classname='collapsible collapsed'
        ),
    ]

    def serve(self, request):
        if not (self.is_zh_finished or self.is_en_finished):
            return redirect('/')
        if request.path.startswith('/en'):
            has_translation = self.is_zh_finished
            other_url = '/zh' + request.path[3:]
            other_language = 'Chinese'
            if not self.is_en_finished:
                return redirect(other_url)
        else:
            has_translation = self.is_en_finished
            other_url = '/en' + request.path[3:]
            other_language = '英文'
            if not self.is_zh_finished:
                return redirect(other_url)
        render_data = locals()
        render_data['page'] = self
        return render(request, 'blog/post_page.html', render_data)


class SearchResultPage(Page):
    def serve(self, request):
        if request.content_type == 'BrythonAjax':
            print('things went here??')
            return HttpResponse('123456')
            # return render(request, 'blog/search_result_ajax.html', dict(result=str(random.randint(10, 50))))

        # if request.method == 'GET':
            # categories = request.GET.get('cats', None)
            # tags = request.GET.get('tags', None)
            # AllPosts = PostPage.objects.filter()

            # need some test
            # for post in PostPage.objects.live().descendant_of(PageFolder):
            #     print(post.tags)
        print('standard render is here!!')

        if request.path.startswith('/en'):
            other_url = '/zh' + request.path[3:]
            other_language = 'Chinese'
        else:
            other_url = '/en' + request.path[3:]
            other_language = '英文'
        has_translation = True
        render_data = locals()
        render_data['page'] = self
        return render(request, 'blog/search_result_page.html', render_data)
