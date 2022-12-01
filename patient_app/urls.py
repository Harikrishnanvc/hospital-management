from django.urls import path
from .views import *
from users.views import sign_in

urlpatterns = [
    path('add-patient/', register_patient_view, name='add-patient'),
    path('register-patient/', RegisterPatientView.as_view(), name='register-patient'),
    path('send-mail/', send_email_after_registration, name='send-mail'),
    path('account-verify/<slug:token>', account_verify, name='account-verify'),
    path('book-appointment-view/<id>', BookAppointmentView.as_view(), name='book-appointment-view'),
    path('book-appointment/<id>', BookAppointmentView.as_view(), name='book-appointment'),
    path('edit-profile_view/', EditProfileView.as_view(), name='editprofileview'),
    path('profile-edit/', EditProfileView.as_view(), name='profile-edit'),
    path('profile-upload/', PatientUploadView.as_view(), name='profile-upload'),
    path('report-view/', PatientUploadView.as_view(), name='scanned_report')

]
