from django.contrib import admin
from .models import LoginCredentials, UserDetails, Doctor, Patient, Leave, Reports, BookAppointment

# Register your models here.
admin.site.register(LoginCredentials)
admin.site.register(UserDetails)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Leave)
admin.site.register(Reports)
admin.site.register(BookAppointment)
