from django.db import models

from django.shortcuts import redirect
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel


class HomePage(Page):
    pass    

class PageFolder(Page):

    def serve(self, request):
        return redirect(request.path[:3])