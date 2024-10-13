from django.urls import path
from . import views

urlpatterns = [
    path('select-language/', views.select_language, name='select_language'),
    path('quiz/<str:language>/<str:level>/', views.quiz_view, name='quiz_view'),
]

