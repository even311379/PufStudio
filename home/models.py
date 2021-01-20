from django.shortcuts import redirect, render, get_object_or_404
from wagtail.core.models import Page
from blog.models import PostPage, MajorCategory
from category.models import Category
from django.db.models import Q


# todo: make pagination
class HomePage(Page):

    def serve(self, request):
        MajorCat = request.GET.get('major_category')
        Cat = request.GET.get('category')
        if request.path.startswith('/en'):
            if MajorCat:
                PostGroupTitle = MajorCategory.objects.get(slug=MajorCat)
                posts = PostPage.objects.live().filter(is_en_finished=True, major_category__slug=MajorCat)
            elif Cat:
                QueryCat = Category.objects.get(name=Cat)
                QD = QueryCat.get_descendants()
                PostGroupTitle = QueryCat.title
                posts = PostPage.objects.live().filter(Q(categories__in=QD) | Q(categories=QueryCat))
            else:
                PostGroupTitle = 'Recent Post'
                posts = PostPage.objects.live().filter(is_en_finished=True)
        else:
            if MajorCat:
                PostGroupTitle = MajorCategory.objects.get(slug=MajorCat)
                posts = PostPage.objects.live().filter(is_zh_finished=True, major_category__slug=MajorCat)
            elif Cat:
                QueryCat = Category.objects.get(name=Cat)
                QD = QueryCat.get_descendants()
                PostGroupTitle = QueryCat.title
                posts = PostPage.objects.live().filter(Q(categories__in=QD) | Q(categories=QueryCat))
            else:
                PostGroupTitle = '近期文章'
                posts = PostPage.objects.live().filter(is_zh_finished=True)
        render_data = locals()
        render_data['page'] = self
        return render(request, 'home/home_page.html', render_data)


class PageFolder(Page):
    subpage_types = ['blog.PostPage', 'apps.AppsPage']

    def serve(self, request):
        return redirect('/' + request.path.split('/')[1])
