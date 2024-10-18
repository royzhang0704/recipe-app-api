""" View for the user API."""
from rest_framework import generics, authentication, permissions
from .serializers import UserSerializer, AuthTokenSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class CreateUserAPIView(generics.CreateAPIView):
    """
    generics.CreateAPIView會專門自動處理POST請求
    """
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """
    serializer_class 使用創建的AuthTokenSerializer 進行驗證 並且會調用authenticate函數驗證是否正確
    render_classes 用來指定渲染模版 一般通常會用Json格式輸出
    """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    視圖的功能是允許用戶查看和更新他們自己的個人資料。
    它使用了 Token 認證和權限檢查，確保只有登入的用戶才能訪問，
    而且用戶只能查看或修改自己的資料，而不能修改其他人的資料。
    """
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """"視圖會基於模型對象的 id 來獲取對應的對象."""
        return self.request.user
