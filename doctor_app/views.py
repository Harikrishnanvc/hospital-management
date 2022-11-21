from django.shortcuts import render, redirect
from django.views.generic import View
from users.models import LoginCredentials, UserDetails, Patient, Reports
from django.db.models import Q

# Create your views here.
class PatientProfileView(View):

    def get(self, request, id):
        try:
            login_details = LoginCredentials.objects.get(id=id)
            user_details = UserDetails.objects.filter(user_details__username=login_details)
            patient_details = Patient.objects.filter(user_details__username=login_details)
            prescription = Reports.objects.filter(user_details__username=login_details)
            context = {
                'login_details': login_details,
                'user_details': user_details,
                'patient_details': patient_details,
                'reports': prescription
            }
            return render(request, 'patient_profile.html', context)

        except LoginCredentials.DoesNotExist:
            return redirect('dashboard')

    def post(self, request, id):
        try:
            patient = LoginCredentials.objects.get(id=id)
            prescription = request.FILES.get('prescription')
            prescription_note = request.POST['prescription_note']
            Reports.objects.create(user_details=patient, prescription=prescription, prescription_note=prescription_note)
            return redirect('patient-profile', id=id)
        except LoginCredentials.DoesNotExist:
            print('not here')
            pass
