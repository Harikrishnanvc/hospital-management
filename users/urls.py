from django.urls import path, include
from .views import (
    dashboard, sign_in, LoginView, sign_out, RegisterDoctorView, register_doctor_view,
    DoctorProfileView, sign_up, ApplyLeaveView, ForgotPasswordView
)


urlpatterns = [
    path('', dashboard, name='dashboard'),
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

]
