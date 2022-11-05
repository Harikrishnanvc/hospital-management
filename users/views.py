from django.shortcuts import render, redirect
from django.views.generic import View
from .models import LoginCredentials, UserDetails, Doctor, Patient
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from .forms import DoctorForm
from django.contrib.auth.hashers import make_password


# Create your views here.

def dashboard(request):
    doctor_details = UserDetails.objects.filter(user_role='doctor')
    doctor_qualification = Doctor.objects.filter()
    print(doctor_qualification)
    context = {'doctor_details': doctor_details,
               'doctor_qualification': doctor_qualification
               }
    return render(request, 'pages/dashboard.html', context)


def sign_in(request):
    return render(request, 'pages/sign-in.html')


def sign_out(request):
    logout(request)
    return redirect('sign-in')


class LoginView(View):

    def post(self, request):
        if request.method == 'POST':
            credentials = request.POST['credentials']
            password = request.POST['password']
            user = authenticate(username=credentials, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.success(request, 'E-mail or Password is incorrect')
                return redirect('sign-in')


def register_doctor_view(request):
    form = DoctorForm()
    return render(request, 'add_doctor.html', {'form': form})


class RegisterDoctorView(View):
    def post(self, request):
        if request.method == 'POST':
            details = DoctorForm(request.POST)
            if details.is_valid():
                email = request.POST['email']
                user_name = request.POST['username']
                phone_number = request.POST['phone_number']
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                department = request.POST['department']
                qualification = request.POST['qualification']
                profile_picture = request.FILES.get('profile_photo')
                random_password = LoginCredentials.objects.make_random_password()
                password = make_password(random_password)

                LoginCredentials.objects.create(email=email, username=user_name, phone_number=phone_number,
                                                password=password)
                try:
                    user = LoginCredentials.objects.get(email=email)
                    UserDetails.objects.create(first_name=first_name, last_name=last_name,
                                               profile_photo=profile_picture, user_details=user, user_role='doctor')
                    Doctor.objects.create(department=department, qualification=qualification, user_details=user)
                    return redirect('dashboard')
                except UserDetails.DoesNotExist:
                    return render(request, 'add_doctor.html')

            return render(request, 'add_doctor.html', {'form': details})
