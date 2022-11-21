from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.base import TemplateView
from .models import LoginCredentials, UserDetails, Doctor, Leave, Patient
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from .forms import DoctorForm
from django.contrib.auth.hashers import make_password


# Create your views here.

def dashboard(request):
    doctor_details = UserDetails.objects.filter(user_role='doctor')
    doctor_qualification = Doctor.objects.filter()
    doctor_login_details = LoginCredentials.objects.filter(userdetails__user_role='doctor')
    patient_details = UserDetails.objects.filter(user_role='patient')
    patient = Patient.objects.filter()
    patient_login_details = LoginCredentials.objects.filter(userdetails__user_role='patient')

    try:
        user_role = UserDetails.objects.get(user_details__username=request.user)
    except UserDetails.DoesNotExist:
        user_role = None
    context = {'doctor_details': doctor_details,
               'doctor_qualification': doctor_qualification,
               'doctor_login_details': doctor_login_details,
               'user_role': user_role,
               'patient_details': patient_details,
               'patient': patient,
               'patient_login_details': patient_login_details,
               }
    return render(request, 'pages/dashboard.html', context)


def sign_in(request):
    return render(request, 'pages/sign-in.html')


def sign_up(request):
    return render(request, 'pages/register.html')


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
                try:
                    user_role = UserDetails.objects.get(user_details__username=user).user_role
                    if user_role == 'doctor':
                        login(request, user)
                        return redirect('dashboard')

                    if user_role == 'admin':
                        login(request, user)
                        return redirect('register-doctor')

                    if user_role == 'patient':
                        try:
                        #     verified_user = Patient.objects.get(user_details__username=user).verify
                        #     if verified_user is True:
                                login(request, user)
                                return redirect('dashboard')
                            # else:
                            #     messages.success(request, f'E-mail is not verified')
                            #     return redirect('sign-in')

                        except Patient.DoesNotExist:
                            messages.success(request, f'{user} does not exist')
                            return redirect('sign-in')

                except UserDetails.DoesNotExist:
                    return redirect('sign-in')
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
                print(random_password)
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


class DoctorProfileView(View):
    def get(self, request):
        login_details = LoginCredentials.objects.filter(username=request.user)
        user_details = UserDetails.objects.filter(user_details__username=request.user)
        doctor_details = Doctor.objects.filter(user_details__username=request.user)
        patient_details = Patient.objects.filter(user_details__username=request.user)

        context = {
            'user_details': user_details,
            'login_details': login_details,
            'doctor_details': doctor_details,
            'patient_details': patient_details
        }
        return render(request, 'pages/profile.html', context)


class ApplyLeaveView(View):
    def get(self, request):
        return render(request, 'pages/register.html')

    def post(self, request, *args, **kwargs):
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        email = request.POST['email']
        leave_reason = request.POST['leave_reason']
        leave_type = request.POST['leave_type']
        try:
            user = LoginCredentials.objects.get(username=request.user)
            Leave.objects.create(from_date=from_date, to_date=to_date, leave_type=leave_type,
                                 leave_reason=leave_reason, user_details=user)
            return redirect('dashboard')

        except LoginCredentials.DoesNotExist:
            return redirect('apply-leave')


class ForgotPasswordView(TemplateView):
    template_name = 'pages/otp_validation.html'



class Edit_Doctor_Profile_View(View):

    def get(self,request):
        
            login_details = LoginCredentials.objects.get(username=request.user)
            user_details = UserDetails.objects.get(user_details__username=request.user)
            doctor_details = Doctor.objects.get(user_details=request.user)
            context = {
                'login_details': login_details,
                'user_details': user_details,
                'doctor_details': doctor_details
            }
            return render(request,'editdoctorprofile.html', context)
            # return render(request, "editprofile.html", {'login_details':login_details,'user_details':user_details,'patient_details':patient_details})
        
    def post(self,request):
        # login_details = UpdateProfileForm()
        # user_details = UpdateUserForm(request.POST,request.FILES)
        # patient_details = UpdatePatientForm()
      
        if request.method == 'POST':
            try:
                login_details = LoginCredentials.objects.get(username=request.user)
      
                user_details = UserDetails.objects.get(user_details__username=request.user)
           
                doctor_details = Doctor.objects.get(user_details=request.user)
                
                login_details.username = request.POST['username']
                login_details.email = request.POST['email']
                login_details.phone_number = request.POST['phone_number']
                user_details.first_name = request.POST['first_name']
                user_details.last_name = request.POST['last_name']
                profile_photo = request.FILES.get('profile_photo')
                doctor_details.qualification = request.POST['qualification']
            
                if profile_photo is None:
                                     
                    
                    user_details.profile_photo = user_details.profile_photo
                    login_details.save()
                    user_details.save()
                    doctor_details.save()

                    messages.success(request,"updated successfully")
                    return redirect('doctor-profile')
                elif profile_photo is not None:
                    user_details.profile_photo = profile_photo
                    login_details.save()
                    user_details.save()
                    doctor_details.save()

                    messages.success(request,"updated successfully")
                    return redirect('doctor-profile')
                else:
                     messages.success(request,"error")
            except:
                return render(request,'editdoctorprofile.html')
