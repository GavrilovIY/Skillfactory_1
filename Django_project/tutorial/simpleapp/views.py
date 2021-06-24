from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView  # импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Product, Category
from .filters import ProductFilter
from .forms import ProductForm
# from datetime import datetime


class Products(ListView):
    model = Product  # указываем модель, объекты которой мы будем выводить
    template_name = 'products.html'  # указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'products'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    ordering = ['-price']
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())
        return context


class ProductDetailView(DetailView):
    template_name = 'simpleapp/product_detail.html'
    queryset = Product.objects.all()


class ProductCreateView(CreateView):
    template_name = 'simpleapp/product_create.html'
    form_class = ProductForm


class ProductUpdateView(UpdateView):
    template_name = 'simpleapp/product_create.html'
    form_class = ProductForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Product.objects.get(pk=id)


class ProductDeleteView(DeleteView):
    template_name = 'simpleapp/product_delete.html'
    queryset = Product.objects.all()
    success_url = '/products/'


# class ProductDetail(DetailView):
#     model = Product
#     template_name = 'product.html'
#     context_object_name = 'product'
