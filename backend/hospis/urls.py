from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Submit your refresh token to this path to obtain a new access token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Path to obtain a new access and refresh token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/', include('hospitalis.urls')),
]
