from django.shortcuts import redirect, render, get_object_or_404
from wagtail.core.models import Page
from blog.models import PostPage




class HomePage(Page):
    def serve(self, request):
        if request.path.startswith('/en'):
            other_url = request.path.replace('/en', '/zh-hant')
            other_language = 'Chinese'
            posts = PostPage.objects.live().filter(is_en_finished=True)
            posts = []
        else:
            other_url = request.path.replace('/zh-hant', '/en')
            other_language = '英文'
            posts = PostPage.objects.live().filter(is_zh_finished=True)
            posts = []
        has_translation = True
        render_data = locals()
        render_data['page'] = self
        return render(request, 'home/home_page.html', render_data)


class PageFolder(Page):
    def serve(self, request):
        return redirect('/' + request.path.split('/')[1])




