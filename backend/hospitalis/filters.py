import django_filters

from .models import ExaminationAction

class ExaminationActionFilter(django_filters.FilterSet):

    class Meta:
        model = ExaminationAction
        fields = ['is_action_paid', 'action_manager']