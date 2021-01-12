
from django.db import models
from django.shortcuts import render, redirect
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase, Tag as TaggitTag
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, FieldRowPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtailorderable.models import Orderable
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from wagtailcodeblock.blocks import CodeBlock

import datetime
from category.models import Category

@register_snippet
class MajorCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug')
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "MajorCategory"
        verbose_name_plural = "MajorCategories"

# @register_snippet
# class TestModel(models.Model, Orderable):
#     test = models.CharField(max_length=30)
#
#     panels = [
#         FieldPanel('test'),
#     ]
#
#     class Meta:
#         ordering=('sort_order')


# @register_snippet
class VVV(Orderable, models.Model):
    ved = models.CharField(max_length=30)

    panels = [
        FieldPanel('ved'),
    ]

    # class Meta:
    #     ordering=('sort_order',)


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


@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True


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
    major_category = models.ForeignKey('MajorCategory', on_delete=models.SET_NULL, blank=True, null=True)
    categories = models.ForeignKey('category.Category', on_delete=models.SET_NULL, blank=True, null=True)
    tags = ClusterTaggableManager(through='PostTag', blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle', classname="full"),
        StreamFieldPanel('body'),
        MultiFieldPanel([
            FieldPanel('major_category'),
            FieldPanel('categories'),
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

    search_fields = Page.search_fields + [
        index.SearchField('subtitle'),
        index.FilterField('is_zh_finished'),
        index.FilterField('is_en_finished'),
    ]

    def serve(self, request):
        if not (self.is_zh_finished or self.is_en_finished):
            return redirect('/')
        if request.path.startswith('/en'):
            has_translation = self.is_zh_finished
            other_url = request.path.replace('/en', '/zh-hant')
            other_language = 'zh-hant'
            if not self.is_en_finished:
                return redirect(other_url)
        else:
            has_translation = self.is_en_finished
            other_url = request.path.replace('/zh-hant', '/en')
            other_language = '英文'
            if not self.is_zh_finished:
                return redirect(other_url)
        render_data = locals()
        render_data['page'] = self
        return render(request, 'blog/post_page.html', render_data)


class SearchResultPage(Page):
    def serve(self, request):
        if request.content_type == 'BrythonAjax':
            keyword = request.GET.get('keyword')

            if request.path.startswith('/en'):
                Posts = PostPage.objects.live().filter(is_en_finished=True).search(keyword)
            else:
                Posts = PostPage.objects.live().filter(is_zh_finished=True).search(keyword)
            return render(request, 'blog/search_result_ajax.html', dict(posts=Posts))


        if request.path.startswith('/en'):
            other_url = request.path.replace('/en', '/zh-hant')
            other_language = 'zh-hant'
        else:
            other_url = request.path.replace('/zh-hant', '/en')
            other_language = '英文'
        has_translation = True
        render_data = locals()
        render_data['page'] = self
        return render(request, 'blog/search_result_page.html', render_data)


class CategorySearchPage(Page):
    def serve(self, request):
        category_slug = request.GET.get('category', '')
        QueryCat = Category.objects.filter(name=category_slug).first()
        if QueryCat:
            QD = QueryCat.get_descendants()
            posts = PostPage.objects.live().filter(models.Q(categories__in=QD)|models.Q(categories=QueryCat))
        render_data = locals()
        render_data['page'] = self
        return render(request, 'blog/category_search_page.html', render_data)


