from django.urls import path

from account import views

urlpatterns = [
    path('list_users', views.ListUsersView.as_view()),
    path('update_users/<int:pk>', views.UpdateUserView.as_view()),
    path('signup_view', views.SignUpView.as_view())
]
