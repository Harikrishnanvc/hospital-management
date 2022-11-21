from django.shortcuts import render, redirect
from django.views.generic import View
from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm
from .forms import PatientForm, UpdateUserForm, UpdateProfileForm, UpdatePatientForm
from django.contrib import messages
from django.contrib.auth import authenticate, login

from users.models import LoginCredentials, UserDetails, Patient, BookAppointment
from users.views import LoginView
from django.db.models import Q

from users.models import LoginCredentials, UserDetails, Patient, ScannedReport
from users.views import LoginView, DoctorProfileView

from django.conf import settings
from django.core.mail import send_mail
import uuid
from django.contrib import messages


# Create your views here.

def send_email_after_registration(email, token):
    user = LoginCredentials.objects.get(email=email)
    subject = 'welcome to email verification'
    message = f'Hi {user.username}, thank you for registering in hospital management.click on the link to varify your account http://127.0.0.1:8000/patient_app/account-verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]
    send_mail(subject, message, email_from, recipient_list)


def account_verify(request, token):
    status = Patient.objects.filter(token=token).first()
    status.verify = True
    status.save()
    return redirect('sign-in')


class EditProfileView(View):

    def get(self, request):

        login_details = LoginCredentials.objects.get(username=request.user)
        user_details = UserDetails.objects.get(user_details__username=request.user)
        patient_details = Patient.objects.get(user_details=request.user)
        context = {
            'login_details': login_details,
            'user_details': user_details,
            'patient_details': patient_details
        }
        return render(request, 'editprofile.html', context)
        # return render(request, "editprofile.html", {'login_details':login_details,'user_details':user_details,'patient_details':patient_details})

    def post(self, request):
        # login_details = UpdateProfileForm()
        # user_details = UpdateUserForm(request.POST,request.FILES)
        # patient_details = UpdatePatientForm()

        if request.method == 'POST':
            try:
                login_details = LoginCredentials.objects.get(username=request.user)

                user_details = UserDetails.objects.get(user_details__username=request.user)

                patient_details = Patient.objects.get(user_details=request.user)

                login_details.username = request.POST['username']
                login_details.email = request.POST['email']
                login_details.phone_number = request.POST['phone_number']
                user_details.first_name = request.POST['first_name']
                user_details.last_name = request.POST['last_name']
                profile_photo = request.FILES.get('profile_photo')
                patient_details.age = request.POST['age']

                if profile_photo is None:

                    user_details.profile_photo = user_details.profile_photo
                    login_details.save()
                    user_details.save()
                    patient_details.save()

                    messages.success(request, "updated successfully")
                    return redirect('doctor-profile')
                elif profile_photo is not None:
                    user_details.profile_photo = profile_photo
                    login_details.save()
                    user_details.save()
                    patient_details.save()

                    messages.success(request, "updated successfully")
                    return redirect('doctor-profile')
                else:
                    messages.success(request, "error")
            except:
                return render(request, 'editprofile.html')

# class EditProfile(View):
#     def get(self,request):
#         login_details = LoginCredentials.objects.get(username=request.user)
#         user_details = UserDetails.objects.get(user_details__username=request.user)
#         patient_details = Patient.objects.get(user_details=request.user)
#         return render(request, "editprofile.html", {'login_details':login_details,'user_details':user_details,'patient_details':patient_details})



def register_patient_view(request):
    form = PatientForm()
    return render(request, 'add_patient.html', {'form': form})


class RegisterPatientView(View):

    def post(self, request):
        if request.method == 'POST':
            details = PatientForm(request.POST)
            token = uuid.uuid4()
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
                                     "your account created successfully to verify your account check your email..")

                    return redirect('sign-in')
                except UserDetails.DoesNotExist:
                    return render(request, 'add_patient.html')

        return render(request, 'add_patient.html', {'form': details})


class BookAppointmentView(View):

    def get(self, request, id):
        doctor_details = LoginCredentials.objects.filter(id=id)
        context = {'doctor_details': doctor_details}
        return render(request, 'book_appointment.html', context)

    def post(self, request, id):
        try:
            user_details = LoginCredentials.objects.get(username=request.user)
            print(user_details)
            doctor_details = LoginCredentials.objects.get(id=id)
            patient_details = UserDetails.objects.get(user_details__username=user_details).get_full_name()
            print(patient_details)
            booking_date = request.POST['booking_date']
            booking_time = request.POST['booking_time']
            appointment = BookAppointment.objects.filter(
                Q(booking_date=booking_date) & Q(booking_time=booking_time) &
                Q(doctor_details=doctor_details)).last()

            if appointment is None:
                token = BookAppointment.objects.filter(Q(booking_date=booking_date) &
                                                       Q(doctor_details=doctor_details)).values('booking_token').last()
                if token is not None:
                    if token['booking_token'] == 0:
                        token = 1

                        BookAppointment.objects.create(user_details=user_details, doctor_details=doctor_details,
                                                       booking_date=booking_date, booking_time=booking_time,
                                                       booking_token=token, booking_name=patient_details)
                        return redirect('dashboard')
                    if token['booking_token'] != 0:
                        if token['booking_token'] < 20:
                            token = token['booking_token'] + 1

                            BookAppointment.objects.create(user_details=user_details, doctor_details=doctor_details,
                                                           booking_date=booking_date, booking_time=booking_time,
                                                           booking_token=token, booking_name=patient_details)
                            return redirect('dashboard')
                        else:
                            messages.error(request, 'No slots available for selected day, please choose another day')
                            return redirect('book-appointment-view', id=id)
                else:
                    token = 1
                    BookAppointment.objects.create(user_details=user_details, doctor_details=doctor_details,
                                                   booking_date=booking_date, booking_time=booking_time,
                                                   booking_token=token, booking_name=patient_details)
                    return redirect('dashboard')
            elif appointment is not None:
                messages.error(request, 'Please select another time')
                return redirect('book-appointment-view', id=id)
        except LoginCredentials.DoesNotExist:
            pass




class PatientUploadView(View):

    def get(self, request):
        # try:
        login_details = LoginCredentials.objects.get(username=request.user)
        user_details = UserDetails.objects.filter(user_details__username=login_details)
        patient_details = Patient.objects.filter(user_details__username=login_details)
        reports = ScannedReport.objects.filter(user_details__username=login_details)
        print(reports)
        context = {
            'login_details': login_details,
            'user_details': user_details,
            'patient_details': patient_details,
            'reports': reports
        }

        return render(request, 'patient_profile_upload.html', context)

    # except:
    #     return redirect('dashboard')
    def post(self, request):
        # try:
        patient = LoginCredentials.objects.get(username=request.user)
        print(patient)
        scanned_report = request.FILES.get('scanned_report')
        ScannedReport.objects.create(user_details=patient, scanned_report=scanned_report)
        return redirect('profile-upload')


