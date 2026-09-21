"""
URL configuration for shadibyaah project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('categories/', views.categories, name='categories'),
path('mehndi-favors/', views.mehndi_favors, name='mehndi_favors'),
path('wedding-favours/', views.wedding_favours, name='wedding_favours'),
path('nikah-essentials/', views.nikah_essentials, name='nikah_essentials'),
path('bridal-shower/', views.bridal_shower, name='bridal_shower'),
path('baby-shower/', views.baby_shower, name='baby_shower'),
path('wedding-cards/', views.wedding_cards, name='wedding_cards'),
path('floral-jewellery/', views.floral_jewellery, name='floral_jewellery'),
path('engagement/', views.engagement, name='engagement'),
path('product/<int:product_id>/', views.product_detail, name='product_detail'),
path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
path('cart/', views.cart, name='cart'),
path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
path('update-cart/<int:product_id>/<str:action>/', views.update_cart, name='update_cart'),
path('checkout/', views.checkout, name='checkout'),
]

