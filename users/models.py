from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserDetails(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    user_id = models.IntegerField(unique=True, null=True)
    user_role = models.CharField(default='admin', max_length=50)
    profile_photo = models.ImageField(upload_to='images', null=True)

    def __str__(self):
        return self.first_name


class LoginCredentials(AbstractUser):
    user_id = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    email = models.CharField(max_length=100, null=True, unique=True)
    phone_number = models.CharField(max_length=100, null=True, unique=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=150)

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = 'Login Credentials'


class Doctor(models.Model):
    user_id = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    qualification = models.CharField(max_length=150)

    def __str__(self):
        return str(self.user_id)


class Patient(models.Model):
    user_id = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    age = models.IntegerField()
    scanned_report = models.FileField(upload_to='scanned_report')
    doctor_report = models.FileField(upload_to='doctor_report')
    prescription = models.FileField(upload_to='prescription')

    def __str__(self):
        return str(self.user_id)
