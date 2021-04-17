from django.urls import path, re_path
from django.conf.urls import url
from twitter import views

app_name = 'twitter'
#url(r'^products/$', 'viewname', name='urlname')
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:twitter_handle>/<str:folder_id>', views.get_twitter_handle, name='get_twitter_handle'),
    url(r'^getwebinars/', views.getwebinars ,name='getwebinars'),


    #path(regex=r'^user/(?P<username>\w{1,50})/$', view='views.get_twitter_handle')
    #re_path(r'^/(?P<twitter_handle>)/(?P<folder_id>)/$', views.get_twitter_handle),
    # path('<str:twitter_handle>/get_webinars/', views.get_webinars, name='get_webinars'),
    # path('<str:twitter_handle>/results/', views.results, name='results'),
]