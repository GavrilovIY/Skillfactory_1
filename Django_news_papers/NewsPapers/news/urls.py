from django.urls import path

from .views import PostList, PostDetail, PostSearch, \
    PostCreateView, PostUpdateView, PostDeleteView  # импортируем наше представление

urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно, почему
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='new'),
    path('search/', PostSearch.as_view(), name='news_search'),
    path('add/',PostCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit', PostUpdateView.as_view(), name='news_update'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='news_delete'),
]