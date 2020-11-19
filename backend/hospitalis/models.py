from django.db import models
import datetime


# Create your models here.
class Doctor(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    # name = models.CharField(max_length=254)
    # date_of_birth = models.DateField(max_length=8, default=datetime.date.today, blank=True)
    # email_field = models.EmailField(max_length=254, default=None)
    # phone_number = models.CharField(max_length=32, blank=True)

    specializes_in = models.CharField(max_length=254, default=None, blank=True)

    # user_active = models.BooleanField(default=True)
    # active_from = models.DateField(default=datetime.date.today)
    #
    # class Meta:
    #     ordering = ['name']
    #     # permission = [()]     TODO: permission group that can access this table will be specified here


class Patient(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    # name = models.CharField(max_length=254)
    # date_of_birth = models.DateField(max_length=8, default=datetime.date.today, blank=True)
    # email_field = models.EmailField(max_length=254, default=None)
    # phone_number = models.CharField(max_length=32, blank=True)

    mainDoctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    # user_active = models.BooleanField(default=True)
    # active_from = models.DateField(default=datetime.date.today)
    #
    # def __str__(self):
    #     return self.name
    #
    # class Meta:
    #     ordering = ['name']
    #     # permission = [()]     TODO: permission group that can access this table will be specified here


class HealthcareWorker(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    # name = models.CharField(max_length=254)
    # date_of_birth = models.DateField(max_length=8, default=datetime.date.today, blank=True)
    # email_field = models.EmailField(max_length=254, default=None)
    # phone_number = models.CharField(max_length=32, blank=True)

    works_for_company = models.CharField(max_length=254, default=None, blank=True)

    # user_active = models.BooleanField(default=True)
    # active_from = models.DateField(default=datetime.date.today)

    # def __str__(self):
    #     return self.name

    # class Meta:
    #     ordering = ['name']
    #     permission = [()]     TODO: permission group that can access this table will be specified here


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

        return self._create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # login:
    email = models.EmailField(max_length=40, unique=True)
    # password inherited

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    username = models.CharField(max_length=30)

    date_of_birth = models.DateField(max_length=8, default=datetime.date.today, blank=True)
    phone_number = models.CharField(max_length=32, blank=True)

    is_active = models.BooleanField(default=True)  # inherited
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    doctor = models.OneToOneField(Doctor, blank=True, null=True, on_delete=models.SET_NULL)
    patient = models.OneToOneField(Patient, blank=True, null=True, on_delete=models.SET_NULL)
    healthcare_worker = models.OneToOneField(HealthcareWorker, blank=True, null=True, on_delete=models.SET_NULL)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


# Zdravotny problem
class HealthConcern(models.Model):
    # Concertn states
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
    description = models.CharField(max_length=2046)
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
    text = models.CharField(max_length=2046)

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
    date_of_examination = models.DateTimeField()
    examinating_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    request_based_on = models.ForeignKey(ExaminationRequest, on_delete=models.CASCADE)
    actions = models.ManyToManyField(ExaminationAction, through='TransactionRequest')

    class Meta:
        ordering = ['date_of_examination']
        # permission = [()]     TODO: permission group that can access this table will be specified here


# Ziadost o zaplatenie jedneho ukonu vramci lekarskeho vysetrenia
class TransactionRequest(models.Model):
    PAID = 'PD'
    UNPAID = 'UD'
    FREE = 'FR'
    TRANSACTION_STATE = [
        (PAID, 'Paid'),
        (UNPAID, 'Unpaid'),
        (FREE, 'Free'),
    ]

    examination = models.ForeignKey(Examination, on_delete=models.CASCADE)
    examination_action = models.ForeignKey(ExaminationAction, on_delete=models.CASCADE)

    transaction_approver = models.ForeignKey(HealthcareWorker, on_delete=models.CASCADE)

    request_state = models.CharField(
        max_length=2,
        choices=TRANSACTION_STATE,
        default=FREE,
    )

    # class Meta:
    # permission = [()]     TODO: permission group that can access this table will be specified here
