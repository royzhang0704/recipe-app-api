from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('create/', views.CreateUserAPIView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
