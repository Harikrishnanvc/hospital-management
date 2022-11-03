from django.contrib import admin
from .models import LoginCredentials, UserDetails, Doctor, Patient

# Register your models here.
admin.site.register(LoginCredentials)
admin.site.register(UserDetails)
admin.site.register(Doctor)
admin.site.register(Patient)
