from django.shortcuts import render, redirect
from django.views.generic import View
from .models import LoginCredentials, UserDetails, Doctor, Patient
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout


# Create your views here.

def dashboard(request):
    return render(request, 'pages/dashboard.html')


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
    return render(request, 'add_doctor.html')


class RegisterDoctorView(View):
    def post(self, request):
        if request.method=='POST':
            username = request.POST['username']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            department = request.POST['department']
            qualification = request.POST['qualification']
            profile_picture = request.POST.FILES['profile_picture']

            print(username,
                  email,
                  first_name,
                  last_name,
                  department,
                  qualification,
                  profile_picture)

        return render(request, 'pages /add_doctor.html')
