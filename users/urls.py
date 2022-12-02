from django.urls import path
from .views import (
    dashboard, sign_in, LoginView, sign_out, RegisterDoctorView, register_doctor_view,

    DoctorProfileView, sign_up, ApplyLeaveView, ForgotPasswordView, OtpValidation, PasswordReset, send_sms,

    DoctorProfileView, sign_up, ApplyLeaveView, ForgotPasswordView, EditDoctorProfileView, BannerView, HomePageView
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home-page'),
    path('dashboard/', dashboard, name='dashboard'),
    path('sign-in', sign_in, name='sign-in'),
    path('login', LoginView.as_view(), name='login'),
    path('sign-out', sign_out, name='sign-out'),
    path('add-doctor/', register_doctor_view, name='add-doctor'),
    path('register-doctor/', RegisterDoctorView.as_view(), name='register-doctor'),
    path('doctor-profile/', DoctorProfileView.as_view(), name='doctor-profile'),
    path('sign-up/', sign_up, name='sign-up'),
    path('apply-leave/', ApplyLeaveView.as_view(), name='apply-leave'),
    path('apply-leave/<pk>', ApplyLeaveView.as_view(), name='send-leave-request'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('otp-generation/', OtpValidation.as_view(), name='otp-generation'),
    path('otp-validation/', OtpValidation.as_view(), name='otp-validation'),
    path('password-reset/', PasswordReset.as_view(), name='password-reset'),
    path('send-sms/', send_sms, name='send-sms'),
    path('edit-doctor-profile_view/', EditDoctorProfileView.as_view(), name='editdoctorprofileview'),
    path('doctor-profile-edit/', EditDoctorProfileView.as_view(), name='doctor-profile-edit'),
    path('view-banner/', BannerView.as_view(), name='banner-view'),
    path('add-banner/', BannerView.as_view(), name='add-banner'),

]
