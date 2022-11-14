from django.urls import path
from .views import *
from users.views import sign_in

urlpatterns = [
       path('add-patient/', register_patient_view, name='add-patient'),
       path('register-patient/', RegisterPatientView.as_view(), name='register-patient'),
       path('send-mail/', send_email_after_registration, name='send-mail'),
       path('account-verify/<slug:token>',account_verify,name='account-verify'),
       path('edit-profilview/',EditProfileView.as_view(),name='editprofileview'),
       path('profile-edit/',EditProfileView.as_view(),name='profile-edit'),



 
  
       

]