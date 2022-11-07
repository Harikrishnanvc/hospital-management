from django import forms
from django.forms import ModelForm
from users.models import LoginCredentials, UserDetails, Patient
from django.core.exceptions import ValidationError


class PatientForm(ModelForm):
    class Meta:
        model = LoginCredentials
        fields = ['email', 'username', 'phone_number']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        db_email = LoginCredentials.objects.filter(email=email).exists()
        if db_email:
            raise ValidationError("email already exist")
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        db_username = LoginCredentials.objects.filter(username=username).exists()
        if db_username:
            raise ValidationError("username already exist")
        return self.cleaned_data

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        db_phone_number = LoginCredentials.objects.filter(phone_number=phone_number).exists()
        if db_phone_number:
            raise ValidationError("phone number already exist")
        return self.cleaned_data
