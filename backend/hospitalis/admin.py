from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import \
    (User,
     Patient,
     Doctor,
     HealthcareWorker,
     HealthConcern,
     DoctorReport,
     ExaminationRequest,
     ExaminationAction,
     Examination,
     TransactionRequest
     )


class DoctorInline(admin.StackedInline):  # TabularInline
    model = Doctor
    can_delete = False
    verbose_name_plural = 'doctors'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (DoctorInline,)  # PatientInline,  HealthcareWorkerInline,


admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(HealthcareWorker)
admin.site.register(User)
admin.site.register(HealthConcern)
admin.site.register(DoctorReport)
admin.site.register(ExaminationRequest)
admin.site.register(ExaminationAction)
admin.site.register(Examination)
admin.site.register(TransactionRequest)
