from django.views.generic import ListView
from .models import Product

# Create your views here.


class ProductsList(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'


