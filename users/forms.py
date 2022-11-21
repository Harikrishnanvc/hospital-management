from django.forms import ModelForm
from django import forms
from .models import LoginCredentials, UserDetails, Doctor
from django.contrib import messages
from django.core.exceptions import ValidationError


class DoctorForm(ModelForm):
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


class PasswordForm(ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = LoginCredentials
        fields = ['password', 'confirm_password']

    def clean(self):
        cleaned_data = super(PasswordForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password not matching"
            )
