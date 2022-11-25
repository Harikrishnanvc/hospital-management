from datetime import datetime

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from users.models import BookAppointment, LoginCredentials


@shared_task
def send_mail_task():
    current_month = datetime.now().month
    doctors = LoginCredentials.objects.filter(userdetails__user_role='doctor')
    for doctor in doctors:
        data = BookAppointment.objects.filter(Q(doctor_details=doctor) &
                                              Q(booking_date__month=current_month))
        merge_data = {
            'data': data
        }
        html_body = render_to_string('mail_template.html', merge_data)
        message = strip_tags(html_body)
        subject = 'Monthly Patient List'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [doctor.email], html_message=html_body)
    return "Mail has been sent........"
