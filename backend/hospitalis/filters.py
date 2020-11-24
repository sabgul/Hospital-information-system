import django_filters

from .models import (
    ExaminationAction,
    Patient,
    HealthConcern,
    ExaminationRequest,
    Examination,
    DoctorReport)


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
        fields = ['main_doctor']


class HealthConcernFilter(django_filters.FilterSet):
    class Meta:
        model = HealthConcern
        fields = ['patient', 'state']


class ExaminationFilter(django_filters.FilterSet):
    class Meta:
        model = Examination
        fields = ['concern']


class DoctorReportFilter(django_filters.FilterSet):
    class Meta:
        model = DoctorReport
        fields = ['about_concern']
