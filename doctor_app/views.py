import os

from django.http import FileResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View

from users.models import BookAppointment, PrescriptionFile
from users.models import LoginCredentials, UserDetails, Patient
from .helpers import save_pdf


# Create your views here.
class PatientProfileView(View):

    def get(self, request, id):
        try:
            login_details = LoginCredentials.objects.get(id=id)
            user_details = UserDetails.objects.filter(user_details__username=login_details)
            patient_details = Patient.objects.filter(user_details__username=login_details)

            reports = PrescriptionFile.objects.filter(user_details__username=login_details)

            context = {
                'login_details': login_details,
                'user_details': user_details,
                'patient_details': patient_details,
                'reports': reports
            }
            return render(request, 'patient_profile.html', context)

        except LoginCredentials.DoesNotExist:
            return redirect('dashboard')

    def post(self, request, id):
        try:
            patient = LoginCredentials.objects.get(id=id)
            patient_instance = Patient.objects.get(user_details=patient)
            prescription = request.FILES.get('prescription')
            prescription_note = request.POST['prescription_note']
            PrescriptionFile.objects.create(user_details=patient, prescription=prescription,
                                            prescription_note=prescription_note, patient=patient_instance)
            return redirect('patient-profile', id=id)
        except LoginCredentials.DoesNotExist:
            return redirect('dashboard')


class BookingList(View):
    def get(self, request):
        doctor_details = UserDetails.objects.filter(user_details__username=request.user)
        patient_booking_list = BookAppointment.objects.filter(doctor_details=request.user)
        booking_details = BookAppointment.objects.filter(user_details__username=request.user)
        context = {
            'doctor_details': doctor_details,
            'patient_booking_list': patient_booking_list,
            'booking_details': booking_details
        }
        return render(request, 'table/compact-table.html', context)


def open_file(request, prescription):
    current = os.getcwd()
    prescription = PrescriptionFile.objects.get(id=prescription).prescription

    f = open(f'{current}/media/prescription/Screenshot_from_2022-11-15_16-16-33_y24gd3s.png', 'rb')

    if f.mode == 'r':
        contents = f.read()
        print(contents)
    return HttpResponse(content_type='application/pdf')


class GeneratePdf(View):
    def get(self, request, id):
        booking_details = BookAppointment.objects.filter(id=id)

        params = {
            'booking_details': booking_details

        }
        file_name, status = save_pdf(params)

        if not status:
            return HttpResponse({'status': 400})

        filepath = os.path.join('static', f'{file_name}.pdf')
        return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
