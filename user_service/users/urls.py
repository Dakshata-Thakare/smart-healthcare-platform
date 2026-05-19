from django.urls import path
# from .views import DoctorDashboardView, ProfileView, RegisterView
from .views import *
urlpatterns = [
    path('register/',RegisterView.as_view()), #in the users table we create the users admin,doctor,receptionist,etc.I guess we should only create the admin from this url and not doctor ,patient ,receiptionist
    path('profile/',ProfileView.as_view()), #no need of this api just for authentication understanding created this api

    #welcome apis according to their role
    path('doctor-dashboard/', DoctorDashboardView.as_view()),
    path('patient-dashboard/', PatientDashboardView.as_view()),
    path('admin-dashboard/', AdminDashboardView.as_view()),
    path('receptionist-dashboard/', ReceptionistDashboardView.as_view()),

    path('doctors/create/', CreateDoctorView.as_view()), #doctor entry adding by admin only in the users table
    path('doctors/', DoctorListView.as_view()),
    path('doctors/<int:doctor_id>/update/', UpdateDoctorView.as_view()), #but here we are updating on the basis of id we need to know the id ,i want according name filter out the dr then update this logic need to add in future
    path('doctors/<int:doctor_id>/delete/', SoftDeleteDoctorView.as_view()),

    path('patients/create/', CreatePatientView.as_view()),
    path('patients/', PatientListView.as_view()), #all the patients
    path('patients/<int:patient_id>/', PatientDetailView.as_view()),   #particular patient this also i should change bcause based on id filtering is wrong need to filter based on name with handling all the upper lower case half name scenrio same for doctor i need to implement
    path('patients/<int:patient_id>/update/', UpdatePatientView.as_view()),#here also change needed based on id not good idea
    path('patients/<int:patient_id>/delete/', SoftDeletePatientView.as_view()),
]