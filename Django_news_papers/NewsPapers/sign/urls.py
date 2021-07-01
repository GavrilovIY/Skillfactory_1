from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import upgrade_me

urlpatterns = [
    path('login/', LoginView.as_view(template_name = 'sign/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name = 'sign/logout.html'), name='logout'),
    path('upgrade/', upgrade_me, name = 'upgrade')
]