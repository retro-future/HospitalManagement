from django import forms

from . import models
from .models import Doctor, Patient


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['address', 'profile_pic', 'phone', 'specialization']


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['address', 'profile_pic', 'phone', "symptoms"]
