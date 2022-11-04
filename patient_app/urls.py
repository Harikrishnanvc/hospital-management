from django.urls import path
from .views import *



urlpatterns = [
    path('register-patient/', RegisterPatientView.as_view(), name='register-patient'),

]