from django.urls import path, re_path

from twitter import views

app_name = 'twitter'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:twitter_handle>/<str:folder_id>', views.get_twitter_handle, name='detail'),
    #re_path(r'^/(?P<twitter_handle>)/(?P<folder_id>)/$', views.get_twitter_handle),
    # path('<str:twitter_handle>/get_webinars/', views.get_webinars, name='get_webinars'),
    # path('<str:twitter_handle>/results/', views.results, name='results'),
]