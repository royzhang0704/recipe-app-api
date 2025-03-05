"""
URL configuration for app project.
"""
from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,

)
from django.conf.urls.static import static
from django.conf import settings

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path(
        'admin/',
        admin.site.urls),
    path(
        'api/schema/',
        SpectacularAPIView.as_view(),
        name='api-schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(
            url_name='api-schema'),
        name='api-docs'),
    path(
        'api/user/',
        include('user.urls')),
    path(
        'api/',
        include('recipe.urls')),
    path(
        'api/jwt/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
    path(
        'api/jwt/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
