from django.urls import path
from .views import AppointmentCreateView, AppointmentDetailView, AppointmentListView, DoctorAppointmentsView, DoctorAvailabilityCreateView, DoctorAvailableSlotsView, DoctorPatientsView, PatientAppointmentsView, SoftDeleteAppointmentView, UpdateAppointmentStatusView

urlpatterns = [
    path('doctor-availability/create/',DoctorAvailabilityCreateView.as_view()),
    path('doctor/my-patients/',DoctorPatientsView.as_view()),
    path('create/', AppointmentCreateView.as_view()),
    path('', AppointmentListView.as_view()),
    path('doctor/', DoctorAppointmentsView.as_view()),
    path('patient/', PatientAppointmentsView.as_view()),
    path('<int:appointment_id>/', AppointmentDetailView.as_view()),
    path('<int:appointment_id>/status/',UpdateAppointmentStatusView.as_view()),
    path('<int:appointment_id>/delete/',SoftDeleteAppointmentView.as_view()),
    path('doctor/<int:doctor_id>/available-slots/',DoctorAvailableSlotsView.as_view()),
]