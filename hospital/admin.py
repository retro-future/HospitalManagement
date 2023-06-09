from django.contrib import admin

from hospital.models import Doctor, Patient, Administrator


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "phone", "specialization")
    list_display_links = ("id", "user")


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "phone")
    list_display_links = ("id", "user")


@admin.register(Administrator)
class AdministratorAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "phone")
    list_display_links = ("id", "user")