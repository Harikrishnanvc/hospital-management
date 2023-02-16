import os

from django.contrib.postgres.search import SearchVector, SearchQuery
from django.db.models import Q
from django.http import FileResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View

from doctor_app.helpers import save_pdf
from users.models import (
    LoginCredentials, UserDetails, Patient,
    Leave, BookAppointment, PrescriptionFile, ScannedReport
)
from haystack.query import SearchQuerySet

# Create your views here.
class PatientProfileView(View):

    def get(self, request, id):
        try:
            login_details = LoginCredentials.objects.get(id=id)
            user_details = UserDetails.objects.filter(user_details__username=login_details)
            patient_details = Patient.objects.filter(user_details__username=login_details)

            reports = PrescriptionFile.objects.filter(patient__user_details=login_details)
            scanned_report = ScannedReport.objects.filter(user_details=login_details)

            context = {
                'login_details': login_details,
                'user_details': user_details,
                'patient_details': patient_details,
                'reports': reports,
                'scanned_report': scanned_report
            }
            return render(request, 'patient_profile.html', context)

        except LoginCredentials.DoesNotExist:
            return redirect('dashboard')

    def post(self, request, id):
        try:
            patient = Patient.objects.get(user_details__id=id)
            doctor = LoginCredentials.objects.get(username=request.user)
            prescription = request.FILES.get('prescription')
            prescription_note = request.POST['prescription_note']
            PrescriptionFile.objects.create(user_details=doctor, prescription=prescription,
                                            prescription_note=prescription_note, patient=patient)
            return redirect('patient-profile', id=id)
        except LoginCredentials.DoesNotExist:
            return redirect('dashboard')


class BookingList(View):
    @staticmethod
    def get(request):
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
    file = PrescriptionFile.objects.get(id=prescription).prescription
    f = open(f'{current}/media/{file}', 'rb')
    if f.mode == 'rb':
        f.readlines()
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


class LeaveStatus(View):
    def post(self, request, pk):
        status = request.POST.get('status')
        if status == 'accepted':
            Leave.objects.filter(id=pk).update(leave_approval='True')
        else:
            Leave.objects.filter(id=pk).update(leave_approval='False')

        return redirect('dashboard')


class SearchView(View):

    def post(self, request):
        query = request.POST.get('search_query')
        try:
            user = UserDetails.objects.get(user_details__username=request.user)

            if user.user_role == 'admin':
                qs = UserDetails.objects.annotate(
                    search=SearchVector("first_name", "last_name") +
                    SearchVector("user_details__doctor__department", "user_role")).filter(
                    search=SearchQuery(query)).exclude(user_role='admin')

            elif user.user_role == 'doctor':
                qs = UserDetails.objects.annotate(
                    search=SearchVector("first_name", "last_name") +
                    SearchVector("user_role")).filter(
                    Q(search=SearchQuery(query)) & ~Q(user_role='doctor') & ~Q(user_role='admin'))

            elif user.user_role == 'patient':
                qs = UserDetails.objects.annotate(
                    search=SearchVector("first_name", "last_name") +
                    SearchVector("user_details__doctor__department", "user_role")).filter(
                    Q(search=SearchQuery(query)) & ~Q(user_role='patient') & ~Q(user_role='admin'))
            else:
                return HttpResponse('No match found')

            return render(request, 'pages/base.html', {'context': qs})

        except UserDetails.DoesNotExist:
            return HttpResponse('Please Login')


def search_titles(request):
    if request.method == 'POST':
        content = request.POST.get('search_text')
    else:
        content = ''

    search = SearchQuerySet.autocomplete(content_auto=content)

    return render(request, 'search/search_results.html', {'content': search})