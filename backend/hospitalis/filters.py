import django_filters

from .models import ExaminationAction, Patient, HealthConcern, ExaminationRequest


class ExaminationActionFilter(django_filters.FilterSet):
    class Meta:
        model = ExaminationAction
        fields = ['is_action_paid', 'action_manager']


class ExaminationRequestFilter(django_filters.FilterSet):
    class Meta:
        model = ExaminationRequest
        fields = ['state']


class PatientsFilter(django_filters.FilterSet):
    class Meta:
        model = Patient
        fields = ['mainDoctor']


class HealthConcernFilter(django_filters.FilterSet):
    class Meta:
        model = HealthConcern
        fields = ['patient']
