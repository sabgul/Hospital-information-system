from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView)

from .settings import BASE_DIR, DEBUG, MEDIA_URL, MEDIA_ROOT

from hospitalis.views import (
    MyObtainTokenPairView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Submit your refresh token to obtain a new access token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Obtain a new access and refresh token
    path('api/token/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    # App data
    path('api/', include('hospitalis.urls')),
    # also works as a login page, currently unused
    path('api-auth/', include('rest_framework.urls')),
]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

