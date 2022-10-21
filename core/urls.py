from django.urls import include, path

from .views import views


urlpatterns = [
    path('', views.index, name=views.index.pattern_name),
]
