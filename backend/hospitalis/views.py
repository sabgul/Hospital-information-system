import django_filters

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework import filters
from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import FileUploadParser

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
    HealthcareWorkerRegSerializer,
    HealthConcernSerializer,
    MyTokenObtainPairSerializer,
    PatientSerializer,
    PatientRegSerializer,
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


class ActionBasedPermission(AllowAny):
    """
    Manage permissions based on lists in ViewSets.

    Used fields
        .action_permissions for checking permissions on the action/method
            (Doctors can list patients)

        .action_object_permissions for checking permissions on the target object
            (Doctor can retrieve examination requests assigned to them)
    """

    def has_permission(self, request, view):
        for klass, actions in getattr(view, 'action_permissions', {}).items():
            if view.action in actions:
                if klass().has_permission(request, view):
                    return True
        return False

    def has_object_permission(self, request, view, obj):
        for klass, actions in getattr(view, 'action_object_permissions', {}).items():
            if view.action in actions:
                if klass().has_object_permission(request, view, obj):
                    return True
        return False


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            return bool(user.doctor)
        except AttributeError:
            return False


class IsHCWorker(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            return bool(user.healthcareworker)
        except AttributeError:
            return False


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if type(obj) == User:
            return obj == request.user
        else:
            return bool(obj.user and obj.user == request.user)


class IsAboutPatient(BasePermission):
    def has_object_permission(self, request, view, obj):
        permission = False

        if type(obj) == HealthConcern:
            try:
                user = obj.patient.user
                permission = bool(user and user == request.user)
            except AttributeError:
                print(exc, file=sys.stderr)

        elif type(obj) == DoctorReport:
            try:
                user = obj.about_concern.patient.user
                permission = bool(user and user == request.user)
            except AttributeError:
                print(exc, file=sys.stderr)

        elif type(obj) == ExaminationRequest:
            try:
                user = obj.concern.patient.user
                permission = bool(user and user == request.user)
            except AttributeError:
                print(exc, file=sys.stderr)

        elif type(obj) == Examination:
            try:
                user = obj.concern.patient.user
                permission = bool(user and user == request.user)
            except AttributeError:
                print(exc, file=sys.stderr)

        elif type(obj) == TransactionRequest:
            try:
                user = obj.related_to_patient.patient.user
                permission = bool(user and user == request.user)
            except AttributeError:
                print(exc, file=sys.stderr)

        return permission


class IsFromDoctor(BasePermission):
    def has_object_permission(self, request, view, obj):
        permission = False

        if type(obj) == HealthConcern:
            print('concern')
            try:
                assigned_doctor_user = obj.doctor.user
                main_doctor_user = obj.patient.main_doctor.user
                permission = request.user in {assigned_doctor_user, main_doctor_user}
            except Exception as exc:
                print(exc, file=sys.stderr)

        elif type(obj) == DoctorReport:
            try:
                user = obj.created_by.user
                permission = bool(user and user == request.user)
            except Exception as exc:
                print(exc, file=sys.stderr)
        elif type(obj) == ExaminationRequest:
            try:
                assigned = obj.assigned_to.user
                created = obj.created_by.user
                permission = bool(created and created == request.user) \
                             or bool(assigned and assigned == request.user)
            except Exception as exc:
                print(exc, file=sys.stderr)
        elif type(obj) == Examination:
            try:
                examinating = obj.examinating_doctor.user
                assigned = obj.request_based_on.assigned_to.user
                from_user = obj.concern.patient.main_doctor.user

                permission = bool(examinating and examinating == request.user) \
                             or bool(assigned and assigned == request.user) \
                             or bool(from_user and from_user == request.user)

            except Exception as exc:
                print(exc, file=sys.stderr)
        elif type(obj) == TransactionRequest:
            try:
                user = obj.related_to_patient.main_doctor.user
                permission = bool(user and user == request.user)
            except Exception as exc:
                print(exc, file=sys.stderr)

        return permission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_staff)


class IsCreationOrIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        # anonymous user can create an account (POST --> view action 'create')
        # for other actions, they must be logged in
        return view.action == 'create' or request.user.is_authenticated


# not a ViewSet
class MyObtainTokenPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = (AllowAny,)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        AllowAny: ['create'],
        IsAuthenticated: ['me'],
        IsOwner: ['destroy', 'partial_update', 'retrieve', 'update'],
        IsAdmin: ['destroy', 'list', 'partial_update', 'retrieve', 'update'],
    }

    action_object_permissions = {
        IsOwner: ['destroy', 'partial_update', 'retrieve', 'update'],
        IsAdmin: ['destroy', 'list', 'partial_update', 'retrieve', 'update'],
    }

    @staticmethod
    def create_user_internal(request):
        reg_user = UserRegSerializer(data=request.data)
        reg_user.is_valid(raise_exception=True)

        user = reg_user.save()
        user.set_password(request.data['password'])
        user.save()  # save again with hashed password

        return reg_user, user

    def create(self, request, *args, **kwargs):
        reg_user, user = self.__class__.create_user_internal(request)
        return Response(reg_user.data, status=status.HTTP_201_CREATED)

    # GET /api/users/me/
    @action(methods=['get'], detail=False)
    def me(self, request, *args, **kwargs):
        user = get_user_model()
        obj = get_object_or_404(user, pk=request.user.id)
        retrieve_me = self.get_serializer(obj)
        return Response(retrieve_me.data)


class PatientsViewSet(ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filter_class = PatientsFilter
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        AllowAny: ['create'],
        IsDoctor: ['list', 'retrieve', 'partial_update', 'update'],
        IsOwner: ['destroy', 'partial_update', 'retrieve', 'update'],
        IsAdmin: ['destroy', 'list', 'partial_update', 'retrieve', 'update'],
    }

    action_object_permissions = {
        IsDoctor: ['list', 'retrieve', 'partial_update', 'update'],
        IsOwner: ['destroy', 'partial_update', 'retrieve', 'update'],
        IsAdmin: ['destroy', 'partial_update', 'retrieve', 'update'],
    }

    def create(self, request, *args, **kwargs):
        # prevent FE from setting any role info
        request.data['doctor'] = None
        request.data['patient'] = None
        request.data['healthcareworker'] = None

        reg_user, user = UserViewSet.create_user_internal(request)
        request.data['user'] = user.id

        try:
            reg_patient = PatientRegSerializer(data=request.data)
            reg_patient.is_valid(raise_exception=True)

            patient = reg_patient.save()
            user.patient = patient
            return Response(reg_patient.data, status=status.HTTP_201_CREATED)
        except Exception as exc:
            # could not create patient (e. g. invalid main_doctor number)
            #  => delete user with no role
            user.delete()

            # propagate error from creating patient instance
            return Response(str(exc), status=status.HTTP_400_BAD_REQUEST)

    # filter LIST results based on role/identity
    def get_queryset(self):
        queryset = self.queryset
        try:
            if self.request.user.doctor and not self.request.user.is_superuser:
                query_set = queryset.filter(main_doctor=self.request.user.doctor)
                return query_set
        except AttributeError:
            return queryset


class DoctorsViewSet(ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsDoctor: ['list', 'retrieve'],
        IsOwner: ['destroy', 'partial_update', 'retrieve', 'update'],
        IsAdmin: ['create', 'destroy', 'list', 'partial_update', 'retrieve', 'update'],
    }

    action_object_permissions = {
        IsDoctor: ['list', 'retrieve'],
        IsOwner: ['destroy', 'partial_update', 'retrieve', 'update'],
        IsAdmin: ['destroy', 'partial_update', 'retrieve', 'update'],
    }

    def create(self, request, *args, **kwargs):
        # prevent FE from setting any role info
        request.data['doctor'] = None
        request.data['patient'] = None
        request.data['healthcareworker'] = None

        reg_user, user = UserViewSet.create_user_internal(request)
        request.data['user'] = user.id

        try:
            reg_doctor = DoctorRegSerializer(data=request.data)
            reg_doctor.is_valid(raise_exception=True)
            doctor = reg_doctor.save()

            user.doctor = doctor
            return Response(reg_doctor.data, status=status.HTTP_201_CREATED)
        except Exception as exc:
            # could not create doctor
            #  => delete user with no role
            user.delete()

            # propagate error from creating doctor instance
            return Response(str(exc), status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            doctor_being_deleted = get_object_or_404(Doctor, pk=kwargs['pk'])
            own_patients = get_list_or_404(Patient, main_doctor=doctor_being_deleted)
            new_doctor_pk = request.query_params['alt']
            new_main_doctor = get_object_or_404(Doctor, pk=new_doctor_pk)

            for patient in own_patients:
                patient.main_doctor = new_main_doctor
                patient.save()

        except:
            # error during transferring patients to new doctor => no patients to transfer, OK
            pass
        return super().destroy(request, args, kwargs)


class HealthcareWorkerViewSet(ModelViewSet):
    queryset = HealthcareWorker.objects.all()
    serializer_class = HealthcareWorkerSerializer
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsOwner: ['destroy', 'partial_update', 'retrieve', 'update'],
        IsAdmin: ['create', 'destroy', 'list', 'partial_update', 'retrieve', 'update'],
        IsHCWorker: ['list'],
    }

    action_object_permissions = {
        IsOwner: ['destroy', 'partial_update', 'retrieve', 'update'],
        IsAdmin: ['destroy', 'partial_update', 'retrieve', 'update'],
    }

    def create(self, request, *args, **kwargs):
        # prevent FE from setting any role info
        request.data['doctor'] = None
        request.data['patient'] = None
        request.data['healthcareworker'] = None

        reg_user, user = UserViewSet.create_user_internal(request)
        request.data['user'] = user.id

        try:
            reg_healthcareworker = HealthcareWorkerRegSerializer(data=request.data)
            reg_healthcareworker.is_valid(raise_exception=True)

            healthcareworker = reg_healthcareworker.save()
            user.healthcareworker = healthcareworker
            return Response(reg_healthcareworker.data, status=status.HTTP_201_CREATED)
        except Exception as exc:
            # could not create hcworker
            #  => delete user with no role
            user.delete()

            # propagate error from creating hcworker instance
            return Response(str(exc), status=status.HTTP_400_BAD_REQUEST)


class HealthConcernViewSet(ModelViewSet):
    queryset = HealthConcern.objects.all()
    serializer_class = HealthConcernSerializer
    filter_class = HealthConcernFilter

    # filter LIST results based on role/identity
    def get_queryset(self):
        queryset = self.queryset

        try:
            if self.request.user.patient and not self.request.user.is_superuser:
                query_set = queryset.filter(patient=self.request.user.patient)
                return query_set
        except AttributeError:
            return queryset

        try:
            if self.request.user.doctor and not self.request.user.is_superuser:
                query_set = queryset.filter(doctor=self.request.user.doctor)
                return query_set
        except AttributeError:
            return queryset

    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAboutPatient: ['list', 'retrieve'],
        IsDoctor: ['create', 'list', 'retrieve'],
        IsFromDoctor: ['destroy', 'partial_update', 'update'],
        IsAdmin: ['create', 'destroy', 'list', 'partial_update', 'retrieve', 'update'],
    }

    action_object_permissions = {
        IsAboutPatient: ['retrieve'],
        IsDoctor: ['retrieve'],
        IsFromDoctor: ['destroy', 'partial_update', 'update'],
        IsAdmin: ['destroy', 'partial_update', 'retrieve', 'update'],
    }


class DoctorReportViewSet(ModelViewSet):
    queryset = DoctorReport.objects.all()
    serializer_class = DoctorReportSerializer
    filter_class = DoctorReportFilter
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAboutPatient: ['retrieve'],
        IsDoctor: ['create', 'list'],
        IsFromDoctor: ['destroy', 'partial_update', 'retrieve', 'update'],
        IsAdmin: ['create', 'destroy', 'partial_update', 'retrieve', 'update'],
    }

    action_object_permissions = {
        IsAboutPatient: ['retrieve'],
        IsFromDoctor: ['destroy', 'partial_update', 'retrieve', 'update'],
        IsAdmin: ['destroy', 'partial_update', 'retrieve', 'update'],
    }


class ExaminationRequestViewSet(ModelViewSet):
    queryset = ExaminationRequest.objects.all()
    serializer_class = ExaminationRequestSerializer
    filter_class = ExaminationRequestFilter
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAboutPatient: ['retrieve'],
        IsDoctor: ['create', 'list'],
        IsFromDoctor: ['destroy', 'partial_update', 'retrieve', 'update'],
        IsAdmin: ['create', 'destroy', 'list', 'partial_update', 'retrieve', 'update'],
    }

    action_object_permissions = {
        IsAboutPatient: ['retrieve'],
        IsFromDoctor: ['destroy', 'partial_update', 'retrieve', 'update'],
        IsAdmin: ['destroy', 'partial_update', 'retrieve', 'update'],
    }

    # filter LIST results based on role/identity
    def get_queryset(self):
        queryset = self.queryset
        try:
            if self.request.user.doctor and not self.request.user.is_superuser:
                query_set = queryset.filter(assigned_to=self.request.user.doctor)
                return query_set
        except AttributeError:
            return queryset


class ExaminationActionViewSet(ModelViewSet):
    queryset = ExaminationAction.objects.all()
    serializer_class = ExaminationActionSerializer
    filter_class = ExaminationActionFilter
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsDoctor: ['list', 'retrieve'],
        IsHCWorker: ['create', 'destroy', 'list', 'partial_update', 'retrieve', 'update'],
        IsAdmin: ['create', 'destroy', 'list', 'partial_update', 'retrieve', 'update'],
    }

    action_object_permissions = {
        IsDoctor: ['list', 'retrieve'],
        IsHCWorker: ['destroy', 'list', 'partial_update', 'retrieve', 'update'],
        IsAdmin: ['destroy', 'partial_update', 'retrieve', 'update'],
    }


class ExaminationViewSet(ModelViewSet):
    queryset = Examination.objects.all()
    serializer_class = ExaminationSerializer
    filter_class = ExaminationFilter
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAboutPatient: ['retrieve'],
        IsDoctor: ['create', 'list'],
        IsFromDoctor: ['retrieve', 'destroy', 'partial_update', 'retrieve', 'update'],
        IsAdmin: ['create', 'destroy', 'list', 'partial_update', 'retrieve', 'update'],
    }

    action_object_permissions = {
        IsAboutPatient: ['retrieve'],
        IsFromDoctor: ['retrieve', 'destroy', 'partial_update', 'retrieve', 'update'],
        IsAdmin: ['destroy', 'partial_update', 'retrieve', 'update'],
    }

    # filter LIST results based on role/identity
    def get_queryset(self):
        queryset = self.queryset
        try:
            if self.request.user.doctor and not self.request.user.is_superuser:
                query_set = queryset.filter(examinating_doctor=self.request.user.doctor)
                return query_set
        except AttributeError:
            return queryset


class TransactionRequestViewSet(ModelViewSet):
    queryset = TransactionRequest.objects.all()
    serializer_class = TransactionRequestSerializer
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAboutPatient: ['retrieve'],
        IsDoctor: ['create'],
        IsFromDoctor: ['retrieve', 'destroy', 'partial_update', 'retrieve', 'update'],
        IsHCWorker: ['destroy', 'list', 'partial_update', 'retrieve', 'update'],
        IsAdmin: ['create', 'destroy', 'list', 'partial_update', 'retrieve', 'update'],
    }

    action_object_permissions = {
        IsAboutPatient: ['retrieve'],
        IsFromDoctor: ['retrieve', 'destroy', 'partial_update', 'retrieve', 'update'],
        IsHCWorker: ['destroy', 'list', 'partial_update', 'retrieve', 'update'],
        IsAdmin: ['destroy', 'list', 'partial_update', 'retrieve', 'update'],
    }

    # filter LIST results based on role/identity
    def get_queryset(self):
        queryset = self.queryset
        try:
            if self.request.user.doctor and not self.request.user.is_superuser:
                query_set = queryset.filter(examinating_doctor=self.request.user.doctor)
                print('filtered', query_set)
                return query_set
        except AttributeError:
            return queryset


