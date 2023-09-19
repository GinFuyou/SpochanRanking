from django.urls import path  # include

from .views import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name=views.index.pattern_name),
]
