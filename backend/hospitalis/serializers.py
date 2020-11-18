from rest_framework.serializers import ModelSerializer

from .models import Patient, Doctor, HealthcareWorker, HealthConcern, DoctorReport, DoctorReportCommentary, ExaminationRequest, ExaminationAction, Examination, TransactionRequest


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


class DoctorReportCommentarySerializer(ModelSerializer):
    class Meta:
        model = DoctorReportCommentary
        fields = '__all__'
        depth = 3


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

    # TODO: This is proper way for nested objects in GET method. Rework everywhere else 
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
