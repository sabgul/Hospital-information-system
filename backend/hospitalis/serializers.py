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


# registration only
class UserRegSerializer(ModelSerializer):
    class Meta(object):
        model = User

        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}


class UserSerializer(ModelSerializer):
    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'doctor', 'patient', 'healthcareworker',
                  # care, you can't see role fields in models.User
                  # OneToOneFields reference User from role-classes, but the connection is both way
                  # the referencing-class name becomes lowercase

                  # 'date_joined'  # , ...
                  )
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

        try:
            if 'role' in self.initial_data:
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
                    if self.user.is_superuser is None:
                        raise AuthenticationFailed()

                else:
                    raise AuthenticationFailed(f'Role \'{role}\' does not exist')

        except (AuthenticationFailed, KeyError, AttributeError) as exc:
            raise AuthenticationFailed('Invalid role: ' + str(exc))

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class DoctorSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

    def to_representation(self, instance):
        # not executed on GET ...:8000/api/doctors/
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        return response


class PatientSerializer(ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        response['mainDoctor'] = DoctorSerializer(instance.mainDoctor).data
        return response


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
