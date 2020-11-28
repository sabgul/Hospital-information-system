from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, UserManager as DefaultBaseUser

import datetime

MALE = 'M'
FEMALE = 'F'
OTHER = 'O'
GENDER = [
    (MALE, 'Male'),
    (FEMALE, 'Female'),
    (OTHER, 'Other'),
]


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(email=email,
                                  username=email,
                                  **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self._create_user(email, password=password, **extra_fields)

        # admin has all the roles
        user.doctor = Doctor.objects.create(user=user, specializes_in='Admin')
        user.healthcareworker = HealthcareWorker.objects.create(user=user, works_for_company='Admin')
        user.patient = Patient.objects.create(user=user, main_doctor=user.doctor)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # login:
    email = models.EmailField(max_length=40, unique=True)
    # password inherited

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, default='username')

    gender = models.CharField(
        max_length=1,
        choices=GENDER,
        default=OTHER,
    )

    objects = UserManager()
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    date_of_birth = models.DateField(max_length=8, default=datetime.date.today, blank=True)
    phone_number = models.CharField(max_length=13, default='', blank=True)

    # Foreign keys:
    # doctor
    # patient
    # healthcareworker

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Doctor(models.Model):
    specializes_in = models.CharField(max_length=254, default=None, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # class Meta:
    #     ordering = ['name']


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    main_doctor = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING)

    # class Meta:
    #     ordering = ['name']


class HealthcareWorker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    works_for_company = models.CharField(max_length=254, default=None, blank=True)

    # class Meta:
    #     ordering = ['name']


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


# Lekarska sprava
class DoctorReport(models.Model):
    created_by = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    about_concern = models.ForeignKey(HealthConcern, on_delete=models.CASCADE)
    date_of_created = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=2046, blank=True)
    file = models.FileField(blank=True, null=True)

    class Meta:
        ordering = ['date_of_created']


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
    assigned_to = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
    created_by = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    state = models.CharField(
        max_length=2,
        choices=REQUEST_STATE,
        default=PENDING,
    )

    class Meta:
        ordering = ['created_timestamp']


# Ukon vramci lekarskeho vysetrenia
class ExaminationAction(models.Model):
    name = models.CharField(max_length=254, primary_key=True)  # To avoid having two similar actions in db
    is_action_paid = models.BooleanField(default=False)
    action_manager = models.ForeignKey(HealthcareWorker, null=True, on_delete=models.SET_NULL)

    def get_action_paid(self):
        if self.is_action_paid:
            return self.is_action_paid

        return False

    class Meta:
        ordering = ['name']


# Lekarske vysetrenie
class Examination(models.Model):
    date_of_examination = models.DateField(default=datetime.date.today)
    examinating_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    request_based_on = models.ForeignKey(ExaminationRequest, on_delete=models.CASCADE, blank=True, null=True)
    concern = models.ForeignKey(HealthConcern, on_delete=models.CASCADE)
    actions = models.ManyToManyField('ExaminationAction', blank=True)
    description = models.CharField(max_length=2046, blank=True)

    class Meta:
        ordering = ['date_of_examination']


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
    transaction_approver = models.ForeignKey(HealthcareWorker, null=True, on_delete=models.SET_NULL)

    request_state = models.CharField(
        max_length=2,
        choices=TRANSACTION_STATE,
        default=UNPAID,
    )

