# -*- coding: utf-8 -*-
"""spochan_ranking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
"""

from django.contrib import admin
from django.conf import settings
# from django.views.generic.base import TemplateView

from django.urls import include, path

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
]

#if settings.DEBUG :
#    import debug_toolbar
#    urlpatterns.append(path('dj-dt/', include(debug_toolbar.urls)),)
