from rest_framework.serializers import ModelSerializer

from .models import Patient, Doctor, HealthcareWorker, HealthConcern, DoctorReport, DoctorReportCommentary, \
    ExaminationRequest, ExaminationAction, Examination, TransactionRequest

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'doctor', 'patient', 'healthcare_worker',
                  'date_joined', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # added here => part of token (not part of response)
        token['username'] = str(user)
        token['is_doctor'] = 1 if user.doctor else 0
        token['is_patient'] = 1 if user.patient else 0
        token['is_healthcare_worker'] = 1 if user.healthcare_worker else 0

        return token


class DoctorSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'


class PatientSerializer(ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['mainDoctor'] = DoctorSerializer(instance.mainDoctor).data
        return response


class HealthcareWorkerSerializer(ModelSerializer):
    class Meta:
        model = HealthcareWorker
        fields = '__all__'


class HealthConcernSerializer(ModelSerializer):
    class Meta:
        model = HealthConcern
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['patient'] = PatientSerializer(instance.patient).data
        return response


class DoctorReportSerializer(ModelSerializer):
    class Meta:
        model = DoctorReport
        fields = '__all__'
        depth = 2


class DoctorReportCommentarySerializer(ModelSerializer):
    class Meta:
        model = DoctorReportCommentary
        fields = '__all__'
        depth = 3


class ExaminationRequestSerializer(ModelSerializer):
    class Meta:
        model = ExaminationRequest
        fields = '__all__'
        depth = 1


class ExaminationActionSerializer(ModelSerializer):
    class Meta:
        model = ExaminationAction
        fields = '__all__'

    # TODO: This is proper way for nested objects in GET method. Rework everywhere else 
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['action_manager'] = HealthcareWorkerSerializer(instance.action_manager).data
        return response


class ExaminationSerializer(ModelSerializer):
    class Meta:
        model = Examination
        fields = '__all__'
        depth = 2


class TransactionRequestSerializer(ModelSerializer):
    class Meta:
        model = TransactionRequest
        fields = '__all__'
        depth = 2
