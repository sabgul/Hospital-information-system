from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Submit your refresh token to obtain a new access token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Obtain a new access and refresh token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # App data
    path('api/', include('hospitalis.urls')),
    # also works as a login page, currently unused
    path('api-auth/', include('rest_framework.urls')),

    path('user-create/', CreateUserAPIView.as_view()),
    path('user/', UserRetrieveUpdateAPIView.as_view()),
]
