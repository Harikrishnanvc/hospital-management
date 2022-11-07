from django.shortcuts import render
from django.views.generic import View
# Create your views here.



class RegisterPatientView(View):

    def get(self, request):
        return render(request, 'pages/add_patient.html')
        
    def post(self, request):
        if request.method=='POST':
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            age = request.POST['age']
            email=request.POST['email']
            phone_number = request.POST['phone_number']
            password=request.POST['passsword']
            # scan_report = request.POST['scan_report']
            # prescription = request.POST['prescription']
            # doctor_report = request.POST['doctor_report']
            # profile_picture = request.POST.FILES['profile_picture']

            
            # print(username,
            #       first_name,
            #       last_name,
            #       age,
            #       email,
            #       phone_number,
            #       password)
            #     #   scan_report,
            #     #   prescription,
            #     #   doctor_report,
            #     #   profile_picture)

        return render(request, 'pages/add_patient.html')



# class PatientLoginView(View):
#     def get(self, request):
#         return render(request, "pages/patient_login.html")

#     def post(self, request):
#         if request.method == 'POST':
#             username = request.POST['username']
#             password = request.POST['password']

#             print(
#                  username,
#                  password

#                 )
#         return render(request, 'pages/patient_login.html')