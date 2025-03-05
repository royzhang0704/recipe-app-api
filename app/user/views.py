""" View for the user API."""
from rest_framework import (
    generics, authentication, permissions, status, response
)
from .serializers import UserSerializer, AuthTokenSerializer, LoginSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)

        return response.Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'username': user.name
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]

            token = RefreshToken(refresh_token)
            token.blacklist()

            return response.Response({
                "detail": "Successfully logged out."
            }, status=status.HTTP_200_OK)
        except Exception:
            return response.Response({
                "detail": "Invalid token or token already blacklisted."
            }, status=status.HTTP_400_BAD_REQUEST)


class CreateUserAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """"視圖會基於模型對象的 id 來獲取對應的對象."""
        return self.request.user
