from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import dashboard, sign_in, RegisterDoctorView, DoctorProfileView, ApplyLeaveView
from doctor_app.views import PatientProfileView

class TestUrls(SimpleTestCase):

    def test_dashboard_url(self):
        url = reverse('dashboard')
        self.assertEqual(resolve(url).func, dashboard)

    def test_sign_in_url(self):
        url = reverse('sign-in')
        self.assertEqual(resolve(url).func, sign_in)

    def test_register_doctor_view_url(self):
        url = reverse('register-doctor')
        self.assertEqual(resolve(url).func.view_class, RegisterDoctorView)

    def test_doctor_profile_view_url(self):
        url = reverse('doctor-profile')
        self.assertEqual(resolve(url).func.view_class, DoctorProfileView)

    def test_patient_profile_view_url(self):
        url = reverse('patient-profile', args=[1])
        self.assertEqual(resolve(url).func.view_class, PatientProfileView)


