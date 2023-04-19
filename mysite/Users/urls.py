from django.urls import path
from .views import CreateUserAPIView,UsersListView

urlpatterns = [
    path('create-user/', CreateUserAPIView.as_view(), name='create-user'),
    path('users/', UsersListView.as_view(), name='users-list'),
]
