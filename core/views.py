# -*- coding: utf-8 -*-

from celestia.view_container import ViewContainer
from django.utils.decorators import method_decorator
from django.views.decorators.gzip import gzip_page
# from django.views.generic import DetailView
from django.views.generic.base import TemplateView  # , RedirectView

views = ViewContainer()


@method_decorator(gzip_page, name='dispatch')
class IndexView(TemplateView):
    template_name = 'index.html'
    pattern_name = 'index'


views.register_class(IndexView)
