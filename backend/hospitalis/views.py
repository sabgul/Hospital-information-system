import django_filters

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import filters
from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from rest_framework_simplejwt.views import TokenObtainPairView

from .models import (
    Doctor,
    DoctorReport,
    Examination,
    ExaminationRequest,
    ExaminationAction,
    HealthConcern,
    HealthcareWorker,
    Patient,
    TransactionRequest,
    User,
)

from .serializers import (
    DoctorSerializer,
    DoctorReportSerializer,
    ExaminationSerializer,
    ExaminationActionSerializer,
    ExaminationRequestSerializer,
    HealthcareWorkerSerializer,
    HealthConcernSerializer,
    MyTokenObtainPairSerializer,
    PatientSerializer,
    TransactionRequestSerializer,
    UserSerializer,
    UserRegSerializer,
)

from .filters import (
    DoctorReportFilter,
    ExaminationFilter,
    ExaminationActionFilter,
    ExaminationRequestFilter,
    PatientsFilter,
    HealthConcernFilter,
)


class IsCreationOrIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        # anonymous user can create an account
        # logged-in user can do anything
        return view.action == 'create' or IsAuthenticated


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsCreationOrIsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.data
        # different serializer used
        reg_serializer = UserRegSerializer(data=user)
        reg_serializer.is_valid(raise_exception=True)
        reg_serializer.save()  # todo use returned instance to create role-users
        return Response(reg_serializer.data, status=status.HTTP_201_CREATED)

    # allows for GET /api/user/me/
    @action(methods=['get'], detail=False)
    def me(self, request, *args, **kwargs):
        user = get_user_model()
        self.object = get_object_or_404(user, pk=request.user.id)
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)


# not a ViewSet
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
