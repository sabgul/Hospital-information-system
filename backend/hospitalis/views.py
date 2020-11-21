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
    DoctorRegSerializer,
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
        # anonymous user can create an account (POST --> view action 'create')
        # for other actions, they must be logged in
        return view.action == 'create' or request.user.is_authenticated


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsCreationOrIsAuthenticated]

    def create(self, request, *args, **kwargs):
        # different serializer used
        user_reg = UserRegSerializer(data=request.data)
        user_reg.is_valid(raise_exception=True)
        user_reg.save()
        return Response(user_reg.data, status=status.HTTP_201_CREATED)

    # allows for GET /api/user/me/
    @action(methods=['get'], detail=False)
    def me(self, request, *args, **kwargs):
        user = get_user_model()
        self.object = get_object_or_404(user, pk=request.user.id)
        retrieve_me = self.get_serializer(self.object)
        return Response(retrieve_me.data)


# not a ViewSet
class MyObtainTokenPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = (AllowAny,)


class PatientsViewSet(ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filter_class = PatientsFilter
    permission_classes = [IsCreationOrIsAuthenticated]


class DoctorsViewSet(ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsCreationOrIsAuthenticated]

    def create(self, request, *args, **kwargs):
        # prevent FE from setting any role info
        request.data['doctor'] = None
        request.data['patient'] = None
        request.data['healthcareworker'] = None

        # different serializer used
        reg_user = UserRegSerializer(data=request.data)

        reg_user.is_valid(raise_exception=True)
        user = reg_user.save()
        request.data['user'] = user.id

        reg_doctor = DoctorRegSerializer(data=request.data)
        reg_doctor.is_valid(raise_exception=True)
        doctor = reg_doctor.save()

        user.doctor = doctor
        return Response(reg_doctor.data, status=status.HTTP_201_CREATED)


class HealthcareWorkerViewSet(ModelViewSet):
    queryset = HealthcareWorker.objects.all()
    serializer_class = HealthcareWorkerSerializer
    permission_classes = [IsCreationOrIsAuthenticated]


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
