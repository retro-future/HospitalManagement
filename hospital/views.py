from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import render
from .forms import DoctorForm


def create_user(request):
    if request.method == 'POST':
        userForm = UserCreationForm(request.POST)
        doctorForm = DoctorForm(request.POST)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorForm.save(commit=False)
            doctor.user = user
            doctor.save()
            return HttpResponse("User created successfully")
    userForm = UserCreationForm()
    doctorForm = DoctorForm()
    return render(request, 'signUp.html', {'userForm': userForm, 'doctorForm': doctorForm})
