from django.urls import path

from blogs import views

urlpatterns = [
    path('', views.get_blogs, name='get_blogs'),
]