from django.forms import ModelForm
from django import forms
from users.models import LoginCredentials,UserDetails,Patient
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserChangeForm

class PatientForm(ModelForm):
    class Meta:
        model = LoginCredentials
        fields = ['email', 'username', 'phone_number']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        db_email = LoginCredentials.objects.filter(email=email).exists()
        #db_email = LoginCredentials.objects.get(email=email)
        print(db_email)
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

class UpdateUserForm(forms.ModelForm):
    # first_name = forms.CharField(max_length=150, required=True,
    #                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    # last_name = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'class':'form-control'})
    # )
    # class Meta:
        model = UserDetails
        fields = ['first_name','last_name','profile_photo']

class UpdateProfileForm(forms.ModelForm):
    # username = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    # email = forms.EmailField(max_length=150,required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))
    # phone_number = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model =LoginCredentials
        fields = ['username','email','phone_number']

class UpdatePatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['age']
