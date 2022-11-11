from django.urls import path, include
from .views import PatientProfileView

urlpatterns = [
    path('patient-profile/<id>', PatientProfileView.as_view(), name='patient-profile'),
    path('patient-profile/<id>', PatientProfileView.as_view(), name='prescription')
]
