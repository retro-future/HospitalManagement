from django import forms
from .models import Doctor


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['address', 'profile_pic', 'phone', 'specialization']
