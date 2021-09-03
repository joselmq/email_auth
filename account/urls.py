
from django.urls import path

from account import views

urlpatterns = [
    path('rest_view', views.GetUserInfo.as_view()),
    path('signup_view', views.SignUpView.as_view())
]
