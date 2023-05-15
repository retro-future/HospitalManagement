from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.models import Group, User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView

from .forms import DoctorForm, PatientForm, AdministratorForm
from .models import Patient, Doctor


def index(request):
    return render(request, 'index.html')


def success_registration(request):
    return render(request, 'signup/success_registration.html')


def sign_up_page(request):
    return render(request, 'signup/sign_up_as.html')


def review_page(request):
    return render(request, 'signup_review/review_page.html')


class ProfileSignUpReview(AccessMixin, ListView):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.request.user.groups.filter(name="ADMIN").exists():
            return HttpResponseRedirect(reverse_lazy('hospital:index'))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(status=False)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')
        if action == 'approve':
            profile = self.model.objects.get(pk=user_id)
            profile.status = True
            profile.save()
        elif action == 'cancel':
            profile = self.model.objects.get(pk=user_id)
            profile.delete()
        return JsonResponse({"success": True})


class PatientSignUpReview(ProfileSignUpReview):
    template_name = 'signup_review/patients_review.html'
    model = Patient
    context_object_name = 'patient_list'


class DoctorSignUpReview(ProfileSignUpReview):
    template_name = 'signup_review/doctors_review.html'
    model = Doctor
    context_object_name = 'doctor_list'


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
        profile_form = self.second_form_class(self.request.POST, self.request.FILES)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = self.object
            profile_form.save()
            group, _ = Group.objects.get_or_create(name=self.group_name)
            group.user_set.add(self.object)
            return response

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})


class SignUpDoctorView(ProfileSignupView):
    template_name = 'signup/doctor_sign_up.html'
    second_form_class = DoctorForm
    profile_form_key = "doctorForm"
    group_name = "DOCTOR"


class SignUpPatientView(ProfileSignupView):
    template_name = 'signup/patient_sign_up.html'
    second_form_class = PatientForm
    profile_form_key = "patientForm"
    group_name = "PATIENT"


class SignUpAdminView(ProfileSignupView):
    template_name = 'signup/admin_sign_up.html'
    second_form_class = AdministratorForm
    profile_form_key = "adminForm"
    group_name = "ADMIN"


class UserLogin(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('hospital:index')


class ListUsersByGroup(View):
    def get(self, request):
        admins = User.objects.filter(groups__name='ADMIN')
        doctors = User.objects.filter(groups__name='DOCTOR')
        patients = User.objects.filter(groups__name='PATIENT')
        return render(request, 'display_users.html', {'admins': admins, 'doctors': doctors, 'patients': patients})
