from django import forms

from . import models
from .models import Doctor, Patient, Administrator


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['address', 'profile_pic', 'phone', 'specialization']


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['address', 'profile_pic', 'phone', "symptoms"]


class AdministratorForm(forms.ModelForm):
    class Meta:
        model = Administrator
        fields = ['address', 'profile_pic', 'phone']