from django.urls import path

from account import views

urlpatterns = [
    path('rest_view', views.GetUserInfo.as_view()),
    path('signup', views.Signup.as_view())
]
