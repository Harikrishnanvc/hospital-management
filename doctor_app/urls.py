from django.urls import path
from .views import PatientProfileView, BookingList, open_file, GeneratePdf

urlpatterns = [
    path('patient-profile/<id>', PatientProfileView.as_view(), name='patient-profile'),
    path('patient-profile/<id>', PatientProfileView.as_view(), name='prescription'),
    path('booking-list/', BookingList.as_view(), name='booking-list'),
    path('generate-pdf/<id>', GeneratePdf.as_view(), name='booking-id'),
    path('open-file/<prescription>', open_file, name='open-file'),

]
