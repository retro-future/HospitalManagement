from django.urls import path
from hospital.views import SignUpDoctorView, SignUpAdminView, SignUpPatientView, success_registration, sign_up_page

app_name = 'hospital'

urlpatterns = [
    path("register/", sign_up_page, name='register'),
    path("register/doctor", SignUpDoctorView.as_view(), name='register_doctor'),
    path("register/admin", SignUpAdminView.as_view(), name='register_admin'),
    path("register/patient", SignUpPatientView.as_view(), name='register_patient'),
    path("register/success/", success_registration, name='success_page'),
]
