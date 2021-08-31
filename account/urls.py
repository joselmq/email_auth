# from .views import SignupPageView
# from django.contrib import admin
from django.urls import path, include
from account import views


urlpatterns = [
    path('rest_view', views.RestAPIView.as_view())
]
