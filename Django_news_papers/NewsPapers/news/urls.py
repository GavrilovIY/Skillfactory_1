from django.urls import path
from django.views.decorators.cache import cache_page
from .views import PostList, PostDetail, PostSearch, \
    PostCreateView, PostUpdateView, PostDeleteView, CategoryList,CategoryDetail  # импортируем наше представление

urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно, почему
    path('', cache_page(60)(PostList.as_view())),
    path('<int:pk>', PostDetail.as_view(), name='new'),
    path('categories/', cache_page(60*5)(CategoryList.as_view()), name = 'categories'),
    path('categories/<int:pk>', CategoryDetail.as_view(), name = 'category_sub'),
    path('search/', PostSearch.as_view(), name='news_search'),
    path('add/',PostCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit', PostUpdateView.as_view(), name='news_update'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='news_delete'),
]