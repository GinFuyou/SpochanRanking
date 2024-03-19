# -*- coding: utf-8 -*-

from celestia.view_container import ViewContainer, register_view
from django.utils.decorators import method_decorator
from django.views.decorators.gzip import gzip_page
from core.models import Profile
from django.views.generic import DetailView
from django.views.generic.base import TemplateView  # , RedirectView

views = ViewContainer()


@method_decorator(gzip_page, name='dispatch')
class IndexView(TemplateView):
    template_name = 'index.html'
    pattern_name = 'index'

    def get(self, *args, **kwargs):
        print(self.request.user.__class__)
        print(type(self.request.user))
        return super().get(*args, **kwargs)


views.register_class(IndexView)


@register_view(views)
@method_decorator(gzip_page, name='dispatch')
class ProfileView(DetailView):
    template_name = "profile.html"
    model = Profile
    slug_field = "chancode"
    slug_url_kwarg = "chancode"
