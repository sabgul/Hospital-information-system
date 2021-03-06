from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.serializers import (ModelSerializer, ReadOnlyField)

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings


from .models import (
    Doctor,
    DoctorReport,
    Examination,
    ExaminationAction,
    ExaminationRequest,
    HealthcareWorker,
    HealthConcern,
    Patient,
    TransactionRequest,
    User)


# registration only (POST)
class UserRegSerializer(ModelSerializer):
    class Meta(object):
        model = get_user_model()

        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}


class UserSerializer(ModelSerializer):
    class Meta(object):
        model = get_user_model()
        fields = ['id', 'email', 'first_name', 'last_name', 'gender',  'date_of_birth', 'phone_number',
                  'doctor', 'patient', 'healthcareworker',
                  # care, you can't see ^role fields^ in models.User
                  # OneToOneFields reference User from role-classes, but the connection is two-way
                  # the referencing-class name becomes lowercase
                  ]
        extra_kwargs = {'password': {'write_only': True}}

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response


# GET only
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        role = '-'
        try:
            role = self.initial_data['role']
            if role == 'patient':
                if self.user.patient is None:
                    raise AuthenticationFailed()

            elif role == 'doctor':
                if self.user.doctor is None:
                    raise AuthenticationFailed()

            elif role == 'healthcare-worker':
                if self.user.healthcareworker is None:
                    raise AuthenticationFailed()

            elif role == 'admin':
                if not self.user.is_superuser:
                    raise AuthenticationFailed()

            else:
                raise AuthenticationFailed('Role \'{}\' does not exist'.format(role))

        except (AuthenticationFailed, KeyError, AttributeError):
            raise AuthenticationFailed('Invalid role \'{}\' for user'.format(role))

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data


class DoctorRegSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['specializes_in', 'user']


class DoctorSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

    def to_representation(self, instance):
        # not executed on GET api/doctors/
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        return response


class PatientRegSerializer(ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class PatientSerializer(ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        response['main_doctor'] = DoctorSerializer(instance.main_doctor).data
        return response


class HealthcareWorkerRegSerializer(ModelSerializer):
    class Meta:
        model = HealthcareWorker
        fields = ['works_for_company', 'user']


class HealthcareWorkerSerializer(ModelSerializer):
    class Meta:
        model = HealthcareWorker
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data

        return response


class HealthConcernSerializer(ModelSerializer):
    class Meta:
        model = HealthConcern
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['patient'] = PatientSerializer(instance.patient).data
        response['doctor'] = DoctorSerializer(instance.doctor).data

        return response


class DoctorReportSerializer(ModelSerializer):
    class Meta:
        model = DoctorReport
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['about_concern'] = HealthConcernSerializer(instance.about_concern).data
        response['created_by'] = DoctorSerializer(instance.created_by).data

        return response


class ExaminationRequestSerializer(ModelSerializer):
    class Meta:
        model = ExaminationRequest
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['concern'] = HealthConcernSerializer(instance.concern).data
        response['assigned_to'] = DoctorSerializer(instance.created_by).data
        response['created_by'] = DoctorSerializer(instance.created_by).data

        return response


class ExaminationActionSerializer(ModelSerializer):
    class Meta:
        model = ExaminationAction
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['action_manager'] = HealthcareWorkerSerializer(instance.action_manager).data

        return response


class ExaminationSerializer(ModelSerializer):
    class Meta:
        model = Examination
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['examinating_doctor'] = DoctorSerializer(instance.examinating_doctor).data
        response['request_based_on'] = ExaminationRequestSerializer(instance.request_based_on).data
        response['concern'] = HealthConcernSerializer(instance.concern).data

        return response


class TransactionRequestSerializer(ModelSerializer):
    class Meta:
        model = TransactionRequest
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['examination_action'] = ExaminationActionSerializer(instance.examination_action).data
        response['related_to_patient'] = PatientSerializer(instance.related_to_patient).data
        response['transaction_approver'] = HealthcareWorkerSerializer(instance.transaction_approver).data

        return response
