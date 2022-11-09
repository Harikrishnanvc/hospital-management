from django.shortcuts import render, redirect
from django.views.generic import View
from django.forms import ModelForm
from .forms import PatientForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from users.models import LoginCredentials, UserDetails, Patient
from users.views import LoginView

from django.conf import settings
from django.core.mail import send_mail
import uuid


# Create your views here.

def send_email_after_registration(email, token):
    user = LoginCredentials.objects.get(email=email)
    subject = 'welcome to email verification'
    message = f'Hi {user.username}, thank you for registering in hospital management.click on the link to varify your account http://127.0.0.1:8000/patient_app/account-verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]
    send_mail(subject, message, email_from, recipient_list)


def account_verify(request, token):
    print(token)
    status = Patient.objects.filter(token=token).first()
    status.verify = True
    status.save()
    return redirect('sign-in')


def register_patient_view(request):
    form = PatientForm()
    return render(request, 'add_patient.html', {'form': form})


class RegisterPatientView(View):

    def post(self, request):
        if request.method == 'POST':
            details = PatientForm(request.POST)
            token = uuid.uuid4()
            print(token)
            if details.is_valid():
                username = request.POST['username']
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                age = request.POST['age']
                email = request.POST['email']
                phone_number = request.POST['phone_number']
                profile_picture = request.FILES.get('profile_photo')
                password = request.POST['passsword']

                # LoginCredentials.objects.create(email=email,username=username,phone_number=phone_number,password=password)
                LoginCredentials.objects.create_user(email=email, username=username, phone_number=phone_number,
                                                     password=password)
                try:

                    user = LoginCredentials.objects.get(email=email)

                    # UserDetails.objects.create(first_name=first_name,last_name=last_name,age=age,profile_picture=profile_picture,user_details=user,user_role='patient')
                    UserDetails.objects.create(first_name=first_name, last_name=last_name,
                                               profile_photo=profile_picture, user_details=user, user_role='patient')
                    Patient.objects.create(age=age, token=token, user_details=user)
                    send_email_after_registration(user.email, token)
                    messages.success(request,
                                     "your account created successfullu to verify your account check your email..")

                    return redirect('sign-in')
                except UserDetails.DoesNotExist:
                    return render(request, 'add_patient.html')

        return render(request, 'add_patient.html', {'form': details})
