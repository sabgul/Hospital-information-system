from django.urls import path

from rest_framework import routers
from .views import PatientsViewSet

router = routers.DefaultRouter()
router.register('patients', PatientsViewSet)

urlpatterns = router.urls