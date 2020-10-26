from rest_framework.serializers import ModelSerializer

from .models import Patient, Doctor, HealthcareWorker, HealthConcern, DoctorReport, DoctorReportCommentary, ExaminationRequest, ExaminationAction, Examination, TransactionRequest


class DoctorSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'date_of_birth', 'email_field']


class PatientSerializer(ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'name', 'date_of_birth', 'email_field', 'mainDoctor']
        depth = 1


class HealthcareWorkerSerializer(ModelSerializer):
    class Meta:
        model = HealthcareWorker
        fields = ['id', 'name', 'date_of_birth']


class HealthConcernSerializer(ModelSerializer):
    class Meta:
        model = HealthConcern
        fields = ['id', 'name', 'description', 'patient', 'doctor', 'state']
        depth = 1


class DoctorReportSerializer(ModelSerializer):
    class Meta:
        model = DoctorReport
        fields = ['id', 'created_by', 'about_concern', 'date_of_created', 'text']
        depth = 2


class DoctorReportCommentarySerializer(ModelSerializer):
    class Meta:
        model = DoctorReportCommentary
        fields = ['id', 'report', 'text']
        depth = 3


class ExaminationRequestSerializer(ModelSerializer):
    class Meta:
        model = ExaminationRequest
        fields = ['id', 'created_timestamp', 'concern', 'created_by', 'state']
        depth = 1


class ExaminationActionSerializer(ModelSerializer):
    class Meta:
        model = ExaminationAction
        fields = ['name', 'is_action_paid', 'action_manager']
        depth = 1


class ExaminationSerializer(ModelSerializer):
    class Meta:
        model = Examination
        fields = ['id', 'date_of_examination', 'examinating_doctor', 'request_based_on', 'actions']
        depth = 2


class TransactionRequestSerializer(ModelSerializer):
    class Meta:
        model = TransactionRequest
        fields = ['id', 'examination', 'examination_action', 'transaction_approver', 'request_state']
        depth = 2
