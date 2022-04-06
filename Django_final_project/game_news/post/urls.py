from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^my_post/$', views.UserPosts.as_view(), name='my-posts'),
    re_path(r'^my_comments/$', views.UserComments.as_view(), name='my-comments'),
    re_path(r'^(?P<pk>\d+)/add_comment$', views.AddComment, name='add_comment'),
    re_path(r'^(?P<pk>\d+)$', views.PostDetailView.as_view(), name='post-detail'),
   
]

urlpatterns += [
    re_path(r'^my_post/create/$', views.PostCreate.as_view(), name='post_create'),
    re_path(r'^my_post/(?P<pk>\d+)/update/$', views.PostUpdate.as_view(), name='post_update'),
    re_path(r'^my_post/(?P<pk>\d+)/delete/$', views.PostDelete.as_view(), name='post_delete'),
    re_path(r'^my_post/(?P<pk>\d+)/comment_append/$', views.append_comment, name='comment_append'),
    re_path(r'^my_post/(?P<pk>\d+)/comment_delete/$', views.delete_commnet, name='comment_delete'),
]
