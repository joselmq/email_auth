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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework.authtoken import views as r_views

from account import views

from .views import HomePageView
# from ..company.views import CompanyList, CompanyInfo, CompanyCreate, CompanyUpdate, CompanyDelete
from company import views as com_views

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('account.urls')),
    path('signup/', views.signup, name='signup'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='login'), name='logout'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('api-token-auth/', r_views.obtain_auth_token),

    # CRUD
    path('company/', com_views.CompanyList.as_view(template_name="company.html"), name='company'),
    path('company/details/<int:pk>', com_views.CompanyInfo.as_view(template_name="details.html"), name='details'),
    path('company/create', com_views.CompanyCreate.as_view(template_name="create.html"), name='create'),
    path('company/update/<int:pk>', com_views.CompanyUpdate.as_view(template_name="update.html"), name='update'),
    path('company/delete/<int:pk>', com_views.CompanyDelete.as_view(), name='delete'),
]
