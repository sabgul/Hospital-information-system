from django.db import models
import datetime

MALE = 'M'
FEMALE = 'F'
OTHER = 'O'
GENDER = [
    (MALE, 'Male'),
    (FEMALE, 'Female'),
    (OTHER, 'Other'),
]


# Create your models here.
class Doctor(models.Model):
    name = models.CharField(max_length=254)
    date_of_birth = models.DateField(max_length=8, default=datetime.date.today, blank=True)
    gender = models.CharField(
        max_length=1,
        choices=GENDER,
        default=OTHER,
    )

    email_field = models.EmailField(max_length=254, default=None)
    phone_number = models.CharField(max_length=32, blank=True)

    specializes_in = models.CharField(max_length=254, default=None, blank=True)

    user_active = models.BooleanField(default=True)
    active_from = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        # permission = [()]     TODO: permission group that can access this table will be specified here


class Patient(models.Model):
    name = models.CharField(max_length=254)
    date_of_birth = models.DateField(max_length=8, default=datetime.date.today, blank=True)
    gender = models.CharField(
        max_length=1,
        choices=GENDER,
        default=OTHER,
    )

    email_field = models.EmailField(max_length=254, default=None)
    phone_number = models.CharField(max_length=32, blank=True)

    mainDoctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    user_active = models.BooleanField(default=True)
    active_from = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        # permission = [()]     TODO: permission group that can access this table will be specified here


class HealthcareWorker(models.Model):
    name = models.CharField(max_length=254)
    date_of_birth = models.DateField(max_length=8, default=datetime.date.today, blank=True)
    gender = models.CharField(
        max_length=1,
        choices=GENDER,
        default=OTHER,
    )

    email_field = models.EmailField(max_length=254, default=None)
    phone_number = models.CharField(max_length=32, blank=True)

    works_for_company = models.CharField(max_length=254, default=None, blank=True)

    user_active = models.BooleanField(default=True)
    active_from = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        # permission = [()]     TODO: permission group that can access this table will be specified here


# Zdravotny problem
class HealthConcern(models.Model):
    # Concern states
    WAITING = 'WT'
    ONGOING = 'ON'
    TERMINAL = 'TL'
    ENDED = 'ED'
    CONCERN_STATE = [
        (WAITING, 'Waiting'),
        (ONGOING, 'Ongoing'),
        (TERMINAL, 'Terminal'),
        (ENDED, 'Ended'),
    ]

    name = models.CharField(max_length=254)
    description = models.CharField(max_length=2046, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    state = models.CharField(
        max_length=2,
        choices=CONCERN_STATE,
        default=ONGOING,
    )

    class Meta:
        ordering = ['name']
        # permission = [()]     TODO: permission group that can access this table will be specified here


# Lekarska sprava
class DoctorReport(models.Model):
    created_by = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    about_concern = models.ForeignKey(HealthConcern, on_delete=models.CASCADE)
    date_of_created = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=2046, blank=True)

    class Meta:
        ordering = ['date_of_created']
        # permission = [()]     TODO: permission group that can access this table will be specified here


# Komentar k lekarskej sprave
class DoctorReportCommentary(models.Model):
    report = models.ForeignKey(DoctorReport, on_delete=models.CASCADE)
    text = models.CharField(max_length=2046)

    # class Meta:
    # permission = [()]     TODO: permission group that can access this table will be specified here


# Ziadost o lekarske vysetrenie
class ExaminationRequest(models.Model):
    # Examination request states
    PENDING = 'PD'
    CANCELED = 'CD'
    RESOLVED = 'RD'
    REQUEST_STATE = [
        (PENDING, 'Pending'),
        (CANCELED, 'Canceled'),
        (RESOLVED, 'Resolved'),
    ]

    created_timestamp = models.DateTimeField(auto_now_add=True)
    concern = models.ForeignKey(HealthConcern, on_delete=models.CASCADE)
    created_by = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    state = models.CharField(
        max_length=2,
        choices=REQUEST_STATE,
        default=PENDING,
    )

    class Meta:
        ordering = ['created_timestamp']
        # permission = [()]     TODO: permission group that can access this table will be specified here


# Ukon vramci lekarskeho vysetrenia
class ExaminationAction(models.Model):
    name = models.CharField(max_length=254, primary_key=True)  # To avoid having two similar actions in db
    is_action_paid = models.BooleanField(default=False)
    action_manager = models.ForeignKey(HealthcareWorker, on_delete=models.CASCADE)

    def get_action_paid(self):
        if self.is_action_paid:
            return self.is_action_paid

        return False

    class Meta:
        ordering = ['name']
        # permission = [()]     TODO: permission group that can access this table will be specified here


# Lekarske vysetrenie
class Examination(models.Model):
    date_of_examination = models.DateField()
    examinating_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    request_based_on = models.ForeignKey(ExaminationRequest, on_delete=models.CASCADE, blank=True, null=True)
    concern = models.ForeignKey(HealthConcern, on_delete=models.CASCADE)
    actions = models.ManyToManyField('ExaminationAction', blank=True)

    class Meta:
        ordering = ['date_of_examination']
        # permission = [()]     TODO: permission group that can access this table will be specified here


# Ziadost o zaplatenie jedneho ukonu vramci lekarskeho vysetrenia
class TransactionRequest(models.Model):
    COVERED = 'CD'
    UNPAID = 'UD'
    TRANSACTION_STATE = [
        (COVERED, 'Covered'),
        (UNPAID, 'Unpaid'),
    ]

    examination_action = models.ForeignKey(ExaminationAction, on_delete=models.CASCADE)

    related_to_patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    transaction_approver = models.ForeignKey(HealthcareWorker, on_delete=models.CASCADE)

    request_state = models.CharField(
        max_length=2,
        choices=TRANSACTION_STATE,
        default=UNPAID,
    )

    # class Meta:
    # permission = [()]     TODO: permission group that can access this table will be specified here
