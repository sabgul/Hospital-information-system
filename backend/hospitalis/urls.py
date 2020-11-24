from django.urls import path
from rest_framework import routers
from .views import (
    DoctorsViewSet,
    DoctorReportViewSet,
    ExaminationViewSet,
    ExaminationActionViewSet,
    ExaminationRequestViewSet,
    HealthcareWorkerViewSet,
    HealthConcernViewSet,
    PatientsViewSet,
    TransactionRequestViewSet,
    UserViewSet,
)

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('patients', PatientsViewSet)
router.register('doctors', DoctorsViewSet)
router.register('healthcare-workers', HealthcareWorkerViewSet)
router.register('health-concerns', HealthConcernViewSet)
router.register('doctor-reports', DoctorReportViewSet)
router.register('examination-requests', ExaminationRequestViewSet)
router.register('examination-actions', ExaminationActionViewSet)
router.register('examinations', ExaminationViewSet)
router.register('transaction-requests', TransactionRequestViewSet)

urlpatterns = router.urls
