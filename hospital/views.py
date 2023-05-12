from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView

from .forms import DoctorForm, PatientForm
from .models import Patient


def success_registration(request):
    return render(request, 'SignUp/success_registration.html')


def sign_up_page(request):
    return render(request, 'SignUp/sign_up_as.html')


class PatientSignUpReview(ListView):
    template_name = 'signup_review/patient_review.html'
    model = Patient
    context_object_name = 'patient_list'

    def get_queryset(self):
        return Patient.objects.filter(status=False)

    def post(self, request, *args, **kwargs):
        patient = self.model.objects.get(pk=request.POST['patient_id'])
        if "approve" in request.POST:
            patient.status = True
            patient.save()
        elif "cancel" in request.POST:
            patient.delete()
        return HttpResponseRedirect(reverse_lazy('hospital:patient_review'))


class ProfileSignupView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('hospital:success_page')
    profile_form_key = None
    group_name = None
    second_form_class = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.profile_form_key not in context:
            context[self.profile_form_key] = self.second_form_class()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        profile_form = self.second_form_class(self.request.POST, instance=self.object)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = self.object
            profile.save()
            group, _ = Group.objects.get_or_create(name=self.group_name)
            group.user_set.add(profile)
        return response


class SignUpDoctorView(ProfileSignupView):
    template_name = 'SignUp/doctor_sign_up.html'
    second_form_class = DoctorForm
    profile_form_key = "doctorForm"
    group_name = "DOCTOR"


class SignUpPatientView(ProfileSignupView):
    template_name = 'SignUp/patient_sign_up.html'
    second_form_class = PatientForm
    profile_form_key = "patientForm"
    group_name = "PATIENT"


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


class ListUsersByGroup(View):
    def get(self, request):
        admins = User.objects.filter(groups__name='ADMIN')
        doctors = User.objects.filter(groups__name='DOCTOR')
        patients = User.objects.filter(groups__name='PATIENT')
        return render(request, 'display_users.html', {'admins': admins, 'doctors': doctors, 'patients': patients})
