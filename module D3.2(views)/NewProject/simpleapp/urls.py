from django.urls import path
from .views import ProductsList


urlpatters = [
    path('',ProductsList.as_view())
]