from django.urls import path
from hospital.views import SignUpDoctorView, SignUpAdminView, SignUpPatientView, success_registration, sign_up_page, \
    ListUsersByGroup, PatientSignUpReview, index, DoctorSignUpReview, review_page

app_name = 'hospital'

urlpatterns = [
    path("", index, name='index'),
    path("register/", sign_up_page, name='register'),
    path("register/doctor", SignUpDoctorView.as_view(), name='register_doctor'),
    path("register/admin", SignUpAdminView.as_view(), name='register_admin'),
    path("register/patient", SignUpPatientView.as_view(), name='register_patient'),
    path("register/success/", success_registration, name='success_page'),
    path("all-users/", ListUsersByGroup.as_view(), name='all_users'),
    path("review/", review_page, name='review_page'),
    path("review/patients", PatientSignUpReview.as_view(), name='patients_review'),
    path("review/doctors", DoctorSignUpReview.as_view(), name='doctors_review'),
]
