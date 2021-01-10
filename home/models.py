from django.db import models
from django.shortcuts import redirect, render
from wagtail.core.models import Page
from blog.models import PostPage


class HomePage(Page):
    def serve(self, request):
        if request.path.startswith('/en'):
            other_url = '/zh'+request.path[3:]
            other_language = 'Chinese'
            posts = PostPage.objects.live().filter(is_en_finished=True)
        else:
            other_url = '/en'+request.path[3:]
            other_language = '英文'
            posts = PostPage.objects.live().filter(is_zh_finished=True)
        has_translation = True
        render_data = locals()
        render_data['page'] = self
        return render(request, 'home/home_page.html', render_data)


class PageFolder(Page):
    def serve(self, request):
        return redirect(request.path[:3])