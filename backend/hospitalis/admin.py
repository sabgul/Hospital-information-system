from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Patient, Doctor, HealthcareWorker


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
# class UserInline(admin.StackedInline):
#     model = User
#     can_delete = False
#     verbose_name_plural = 'patients'  # I don't understand why this is here

#
class DoctorInline(admin.StackedInline):  # TabularInline
    model = Doctor
    can_delete = False
    verbose_name_plural = 'doctors'
#
#
# class HealthcareWorkerInline(admin.StackedInline):
#     model = HealthcareWorker
#     can_delete = False
#     verbose_name_plural = 'HealthcareWorkers'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (DoctorInline,)  # PatientInline,  HealthcareWorkerInline,


# Re-register UserAdmin
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(HealthcareWorker)
admin.site.register(User)
# admin.site.register(User, UserAdmin)

# Register your models here.
