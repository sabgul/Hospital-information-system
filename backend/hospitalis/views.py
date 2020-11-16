from rest_framework.viewsets import ModelViewSet
import django_filters

from .models import Patient, Doctor, HealthcareWorker, HealthConcern, DoctorReport, DoctorReportCommentary, ExaminationRequest, ExaminationAction, Examination, TransactionRequest
from .serializers import PatientSerializer, DoctorSerializer, HealthcareWorkerSerializer, HealthConcernSerializer, DoctorReportSerializer, DoctorReportCommentarySerializer, ExaminationRequestSerializer, ExaminationActionSerializer, ExaminationSerializer, TransactionRequestSerializer
from .filters import ExaminationActionFilter, PatientsFilter, HealthConcernFilter, ExaminationRequestFilter


class PatientsViewSet(ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filter_class = PatientsFilter


class DoctorsViewSet(ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class HealthcareWorkerViewSet(ModelViewSet):
    queryset = HealthcareWorker.objects.all()
    serializer_class = HealthcareWorkerSerializer


class HealthConcernViewSet(ModelViewSet):
    queryset = HealthConcern.objects.all()
    serializer_class = HealthConcernSerializer
    filter = HealthConcernFilter


class DoctorReportViewSet(ModelViewSet):
    queryset = DoctorReport.objects.all()
    serializer_class = DoctorReportSerializer


class DoctorReportCommentaryViewSet(ModelViewSet):
    queryset = DoctorReportCommentary.objects.all()
    serializer_class = DoctorReportCommentarySerializer


class ExaminationRequestViewSet(ModelViewSet):
    queryset = ExaminationRequest.objects.all()
    serializer_class = ExaminationRequestSerializer
    filter_class = ExaminationRequestFilter


class ExaminationActionViewSet(ModelViewSet):
    queryset = ExaminationAction.objects.all()
    serializer_class = ExaminationActionSerializer
    filter_class = ExaminationActionFilter


class ExaminationViewSet(ModelViewSet):
    queryset = Examination.objects.all()
    serializer_class = ExaminationSerializer


class TransactionRequestViewSet(ModelViewSet):
    queryset = TransactionRequest.objects.all()
    serializer_class = TransactionRequestSerializer
