"""auth_email URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework.authtoken import views as r_views

from account import views

from .views import HomePageView

urlpatterns = [
    # Auth
    path('', HomePageView.as_view(), name='home'),
    path('admin/', admin.site.urls, name='admin'),
    path('users/', include('account.urls'), name='users_urls'),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(template_name='login.html'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('api-token-auth/', r_views.obtain_auth_token, name='api_auth'),
    path('company/', include("company.urls"), name='company_urls')
]
