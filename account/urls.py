from django.urls import path

from account import views

urlpatterns = [
    path('', views.ListUsersView.as_view(), name='list_users'),
    path('<int:pk>/update', views.UpdateUserView.as_view(), name='update_user'),
    path('add', views.SignUpView.as_view(), name='add_user')
]
