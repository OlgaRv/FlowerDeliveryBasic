from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('catalog/', views.catalog, name='catalog'),
    path('order/', views.order, name='order'),
    path('order_success/', views.order_success, name='order_success'),
]
