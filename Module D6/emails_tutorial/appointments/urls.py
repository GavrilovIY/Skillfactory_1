from django.urls import path
from .views import AppointmentView

urlpatterns = [
    path('make_appointments/', AppointmentView.as_view(), name='make_appointments')
]