from django.views.generic import ListView  # импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Product
# from datetime import datetime



class Products(ListView):
    model = Product  # указываем модель, объекты которой мы будем выводить
    template_name = 'products.html'  # указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'products'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    ordering = ['-price']
    paginate_by = 1
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['time_now'] = datetime.utcnow()
#         return context
# #
# class ProductDetail(DetailView):
#     model = Product
#     template_name = 'product.html'
#     context_object_name = 'product'
