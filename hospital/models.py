from enum import Enum

from django.db import models
from django.contrib.auth.models import User


class Specialization(Enum):
    CARDIOLOGIST = 'Cardiologist'
    DERMATOLOGIST = 'Dermatologist'
    DENTIST = 'Dentist'
    ANESTHESIOLOGIST = 'Anesthesiologist'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='profile_pic/DoctorProfilePic/', null=True, blank=True)
    phone = models.CharField(max_length=20, null=True)
    specialization = models.CharField(max_length=100, choices=Specialization.choices())


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='profile_pic/PatientProfilePic/', null=True, blank=True)
    phone = models.CharField(max_length=20, null=True)


class Appointment(models.Model):
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    patientName = models.CharField(max_length=100)
    doctorName = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    status = models.BooleanField(default=False)

