from django.urls import path
# from .views import ProductsList, ProductDetail  # импортируем наше
from .views import Products, ProductDetailView, ProductCreateView, ProductDeleteView, ProductUpdateView

urlpatterns = [
    path('',Products.as_view()),
    path('<int:pk>/', ProductDetailView.as_view(), name = 'product_detail'),
    path('create/', ProductCreateView.as_view(), name = 'product_create'),
    path('create/<int:pk>', ProductUpdateView.as_view(), name='product_update'),
    path('delete/<int:pk>', ProductDeleteView.as_view(), name='product_delete')
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно, почему
    # path('', ProductsList.as_view()),
    # path('<int:pk>', ProductDetail.as_view())
    # т. к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
]