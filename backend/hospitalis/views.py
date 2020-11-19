from rest_framework.viewsets import ModelViewSet
import django_filters
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Patient, Doctor, HealthcareWorker, HealthConcern, DoctorReport, DoctorReportCommentary, \
    ExaminationRequest, ExaminationAction, Examination, TransactionRequest
from .serializers import PatientSerializer, DoctorSerializer, HealthcareWorkerSerializer, HealthConcernSerializer, \
    DoctorReportSerializer, DoctorReportCommentarySerializer, ExaminationRequestSerializer, ExaminationActionSerializer, \
    ExaminationSerializer, TransactionRequestSerializer, MyTokenObtainPairSerializer, UserSerializer
from .filters import ExaminationActionFilter, PatientsFilter, HealthConcernFilter

from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView

from rest_framework.response import Response
from rest_framework import status

""" POST testing
{
    "email": "gah@ma.il",
    "password": "googlegogol"

}

{
    "email": "ja@ja.ja",
    "password": "heslojasam"
}
"""


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    # Allow only authenticated users to access this url
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        serializer = UserSerializer(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateUserAPIView(APIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# obtain token that includes additional field
class MyObtainTokenPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = (AllowAny,)


class PatientsViewSet(ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filter_class = PatientsFilter
    permission_classes = [IsAuthenticated]


class DoctorsViewSet(ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]


class HealthcareWorkerViewSet(ModelViewSet):
    queryset = HealthcareWorker.objects.all()
    serializer_class = HealthcareWorkerSerializer
    permission_classes = [IsAuthenticated]


class HealthConcernViewSet(ModelViewSet):
    queryset = HealthConcern.objects.all()
    serializer_class = HealthConcernSerializer
    # filter = HealthConcernFilter
    permission_classes = [IsAuthenticated]
    filter_class = HealthConcernFilter


class DoctorReportViewSet(ModelViewSet):
    queryset = DoctorReport.objects.all()
    serializer_class = DoctorReportSerializer
    filter_class = DoctorReportFilter
    permission_classes = [IsAuthenticated]


class ExaminationRequestViewSet(ModelViewSet):
    queryset = ExaminationRequest.objects.all()
    serializer_class = ExaminationRequestSerializer
    filter_class = ExaminationRequestFilter
    permission_classes = [IsAuthenticated]


class ExaminationActionViewSet(ModelViewSet):
    queryset = ExaminationAction.objects.all()
    serializer_class = ExaminationActionSerializer
    filter_class = ExaminationActionFilter
    permission_classes = [IsAuthenticated]


class ExaminationViewSet(ModelViewSet):
    queryset = Examination.objects.all()
    serializer_class = ExaminationSerializer
    filter_class = ExaminationFilter
    permission_classes = [IsAuthenticated]


class TransactionRequestViewSet(ModelViewSet):
    queryset = TransactionRequest.objects.all()
    serializer_class = TransactionRequestSerializer
    permission_classes = [IsAuthenticated]
