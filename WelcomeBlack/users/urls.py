# users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # Homepage route
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('welcome/', views.welcome_view, name='welcome'),  # Welcome page
    path('questions/', views.questions_view, name='questions'),
]
