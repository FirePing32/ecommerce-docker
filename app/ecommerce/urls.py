"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from unicodedata import name
from django.contrib import admin
from django.urls import include, path
from store import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('vendor/details/<str:vendor>', views.vendorProfile, name='vendorProfile'),
    path('vendor/login', views.vendorlogin, name='vendorlogin'),
    path('vendor/signup', views.vendorsignup, name='vendorsignup'),
    path('vendor/dashboard', views.vendorDashboard, name='vendorDashboard'),
    path('item/<uuid:uuid>', views.itemView, name='itemView'),
    path('cart/', views.cart, name='cart'),
    path('dashboard', views.userDashboard, name='userDashboard'),
    path('store/', include('store.urls')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
]