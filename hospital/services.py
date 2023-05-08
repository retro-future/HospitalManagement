from django import forms
from django.contrib.auth.forms import UserCreationForm

from hospital.forms import DoctorForm, PatientForm


class BaseService:
    def create_user(self, user_form: forms.ModelForm, profile_form: forms.ModelForm):
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return True
        return False


class DoctorService(BaseService):
    def create_doctor(self, request_data, files_data=None):
        userForm = UserCreationForm(request_data)
        doctorForm = DoctorForm(data=request_data, files=files_data)
        return self.create_user(userForm, doctorForm)


class PatientService(BaseService):

    def create_patient(self, request_data, files_data=None):
        userForm = UserCreationForm(request_data)
        patientForm = PatientForm(data=request_data, files=files_data)
        return self.create_user(userForm, patientForm)
