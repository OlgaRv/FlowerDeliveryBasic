# C:/Users/Ольга/Documents/GitHub/FlowerDeliveryBasic/FlowerDelivery_Basic/main/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('catalog/', views.catalog, name='catalog'),
    path('order/', views.order, name='order'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
    path('account/orders/', views.all_orders, name='all_orders'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

