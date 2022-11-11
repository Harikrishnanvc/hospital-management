from django.urls import path
from .views import *
from users.views import sign_in

urlpatterns = [
       path('add-patient/', register_patient_view, name='add-patient'),
       path('register-patient/', RegisterPatientView.as_view(), name='register-patient'),
       path('send-mail/', send_email_after_registration, name='send-mail'),
       path('account-verify/<slug:token>',account_verify,name='account-verify'),
       path('book-appointment-view/<id>', BookAppointmentView.as_view(), name='book-appointment-view'),
       path('book-appointment/<id>', BookAppointmentView.as_view(), name='book-appointment')

]