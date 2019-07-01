from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='bot-index'),
    path('chatbot/', views.bot),
    path('goodAnswer/', views.goodAnswer)
]