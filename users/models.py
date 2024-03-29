from django.contrib.auth.models import AbstractUser
from django.db import models


class LoginCredentials(AbstractUser):
    email = models.CharField(max_length=100, null=True, unique=True)
    phone_number = models.CharField(max_length=100, null=True, unique=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=150)

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = 'Login Credentials'


class UserDetails(models.Model):
    user_details = models.ForeignKey(LoginCredentials, on_delete=models.CASCADE, null=True, related_name='userdetails')
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    user_role = models.CharField(default='admin', max_length=50)
    profile_photo = models.ImageField(upload_to='images', null=True)

    def __str__(self):
        return self.user_details.username

    def get_full_name(self):
        return ("%s %s" % (self.first_name, self.last_name)).strip()


# Create your models here.


class Doctor(models.Model):
    user_details = models.ForeignKey(LoginCredentials, on_delete=models.CASCADE, null=True, related_name='doctor')
    department = models.CharField(max_length=100)
    qualification = models.CharField(max_length=150)

    def __str__(self):
        return self.user_details.username


class Patient(models.Model):
    user_details = models.ForeignKey(LoginCredentials, on_delete=models.CASCADE, null=True)
    age = models.IntegerField(null=True)
    token = models.CharField(max_length=150, null=True)
    verify = models.BooleanField(null=True, blank=True, default=False)

    def __str__(self):
        return self.user_details.username


class PrescriptionFile(models.Model):
    user_details = models.ForeignKey(LoginCredentials, on_delete=models.CASCADE, null=True)
    prescription = models.FileField(upload_to='prescription', null=True, )
    prescription_note = models.CharField(max_length=150, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user_details.username


class ScannedReport(models.Model):
    user_details = models.ForeignKey(LoginCredentials, on_delete=models.CASCADE, null=True)
    scanned_report = models.FileField(upload_to='scanned_report', null=True)
    prescription_note = models.CharField(max_length=150, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user_details.username


class Leave(models.Model):
    user_details = models.ForeignKey(LoginCredentials, on_delete=models.CASCADE, null=True)
    from_date = models.DateField(null=True)
    to_date = models.DateField(null=True)
    leave_type = models.CharField(max_length=50, null=True)
    leave_reason = models.CharField(max_length=150, null=True)
    leave_approval = models.BooleanField(null=True)

    def __str__(self):
        return self.user_details.username


class BookAppointment(models.Model):
    user_details = models.ForeignKey(LoginCredentials, on_delete=models.CASCADE, null=True)
    doctor_details = models.ForeignKey(LoginCredentials, on_delete=models.CASCADE, null=True,
                                       related_name='doctor_details')
    booking_name = models.CharField(max_length=150, null=True)
    booking_date = models.DateField(null=True)
    booking_time = models.TimeField(null=True)
    booking_token = models.IntegerField(default=0, null=True)
    booking_status = models.BooleanField(default=False)
    expired = models.BooleanField(null=True)

    def __str__(self):
        return self.user_details.username


class Banner(models.Model):
    user_details = models.ForeignKey(LoginCredentials, on_delete=models.CASCADE, null=True)
    banner = models.ImageField(upload_to='banner', null=True)
    caption = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.caption
    