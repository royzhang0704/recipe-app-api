from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('create/', views.CreateUserAPIView.as_view(),
         name='create'),  # localhost:8003/api/user/create
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
