from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import DoctorForm, PatientForm


def success_registration(request):
    return render(request, 'SignUp/success_registration.html')


def sign_up_page(request):
    return render(request, 'SignUp/sign_up_as.html')


class SignUpDoctorView(CreateView):
    template_name = 'SignUp/doctor_sign_up.html'
    form_class = UserCreationForm
    second_form_class = DoctorForm
    success_url = reverse_lazy('hospital:success_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "doctorForm" not in context:
            context["doctorForm"] = self.second_form_class()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        doctorForm = self.second_form_class(self.request.POST, instance=self.object)
        if doctorForm.is_valid():
            doctor = doctorForm.save(commit=False)
            doctor.user = self.object
            doctor.save()
            group, _ = Group.objects.get_or_create(name="DOCTOR")
            group.user_set.add(doctor)
        return response


class SignUpPatientView(CreateView):
    template_name = 'SignUp/patient_sign_up.html'
    form_class = UserCreationForm
    second_form_class = PatientForm
    success_url = reverse_lazy('hospital:success_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "patientForm" not in context:
            context["patientForm"] = self.second_form_class()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        patientForm = self.second_form_class(self.request.POST, instance=self.object)
        if patientForm.is_valid():
            patient = patientForm.save(commit=False)
            patient.user = self.object
            patient.save()
            group, _ = Group.objects.get_or_create(name="PATIENT")
            group.user_set.add(patient)
        return response


class SignUpAdminView(CreateView):
    template_name = 'SignUp/admin_sign_up.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('hospital:success_page')

    def form_valid(self, form):
        admin = form.save(commit=False)
        admin.set_password(admin.password)
        admin.save()
        group, _ = Group.objects.get_or_create(name="ADMIN")
        group.user_set.add(admin)
        return HttpResponseRedirect(reverse_lazy('hospital:success_page'))

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})
