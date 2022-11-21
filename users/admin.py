from django.contrib import admin
from .models import (LoginCredentials, UserDetails, Doctor, Patient, Leave, PrescriptionFile, ScannedReport,
                     BookAppointment,
                     )
from paymentapp.models import Order
# Register your models here.
admin.site.register(LoginCredentials)
admin.site.register(UserDetails)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Leave)
admin.site.register(ScannedReport)
admin.site.register(PrescriptionFile)
admin.site.register(BookAppointment)
admin.site.register(Order)
