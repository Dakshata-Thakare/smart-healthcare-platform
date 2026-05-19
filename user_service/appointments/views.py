from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .utils import generate_time_slots
from  datetime import datetime
from .models import Appointment, DoctorAvailability
from .serializers import AppointmentSerializer, DoctorAvailabilitySerializer, DoctorPatientAppointmentSerializer
from users.permissions import CanAccessAppointment, IsAdmin, IsAdminOrReceptionist, IsDoctor, IsPatient
from .utils import get_available_slots


class DoctorAvailabilityCreateView(APIView):
    print("HIIIIII")
    permission_classes = [IsAuthenticated,IsAdminOrReceptionist] #I guess hee we should give permission to doctor also ,future development
    def post(self, request):
        serializer = DoctorAvailabilitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class DoctorPatientsView(APIView):
    permission_classes = [IsAuthenticated,IsDoctor] #ok only doctor can see his patients list not admin as we are filtering bases doctor=request.user
    def get(self, request):
    #Without select_related  Django performs:1 query for appointments + N queries for patients called: N+1 Query Problem
    # With select_related Django performs:single SQL JOIN query
        appointments = Appointment.objects.filter(doctor=request.user,is_deleted=False ##
        ).select_related('patient','doctor')

        serializer = DoctorPatientAppointmentSerializer(
            appointments,
            many=True
        )

        return Response(serializer.data)

#in this api we should return the avaiable slot based on day and i guess for whole week doctors available slot we should give back
#and we are creating appointments on the week basis that is wrong we should create appointment of any day in 2 months
class AppointmentCreateView(APIView):
    permission_classes = [IsAuthenticated,IsAdminOrReceptionist]
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

 #in this api we should add asc or desc option particulat day filter particular date range filter ,filter of doctor ,filter of patient ,filter of patiend and doctor   
#pagination ,offset limit also
class AppointmentListView(APIView):
    permission_classes = [IsAuthenticated,IsAdminOrReceptionist]

    def get(self, request):

        appointments = Appointment.objects.filter(
            is_deleted=False
        ).select_related(
            'patient',
            'doctor'
        )

        serializer = AppointmentSerializer(
            appointments,
            many=True
        )

        return Response(serializer.data)

# here also pagination and filtering we should add
#bases on completed ,pending ,etc filter on status
#date filter also we should add
# # in the response getting patient id ,doctor id instead of that we should get their name 
class DoctorAppointmentsView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsDoctor
    ]

    def get(self, request):
        print("request.user ,",request.user)
        appointments = Appointment.objects.filter(
            doctor=request.user,
            is_deleted=False
        ).select_related(
            'patient',
            'doctor'
        )
        print("appointments     ",appointments)

        serializer = AppointmentSerializer(
            appointments,
            many=True
        )

        return Response(serializer.data)

# in the response getting patient id ,doctor id instead of that we should get their name
# here also pagination and filtering we should add
#bases on completed ,pending ,etc filter on status
#date filter also we should add
class PatientAppointmentsView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsPatient
    ]

    def get(self, request):

        appointments = Appointment.objects.filter(
            patient=request.user,
            is_deleted=False
        ).select_related(
            'patient',
            'doctor'
        )

        serializer = AppointmentSerializer(
            appointments,
            many=True
        )

        return Response(serializer.data)

#in this api also we are returning appoitment id ,patient id ,doctor id instead we should return name    
class AppointmentDetailView(APIView):
    permission_classes = [
        IsAuthenticated,
        CanAccessAppointment
    ]
    def get(self, request, appointment_id):

        try:

            appointment = Appointment.objects.select_related(
                'patient',
                'doctor'
            ).get(
                id=appointment_id,
                is_deleted=False
            )

        except Appointment.DoesNotExist:

            return Response(
                {"error": "Appointment not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(
            request,
            appointment
        )

        serializer = AppointmentSerializer(
            appointment
        )

        return Response(serializer.data)

class UpdateAppointmentStatusView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrReceptionist
    ]

    def patch(self, request, appointment_id):

        status_value = request.data.get('status')

        allowed_status = [
            'CONFIRMED',
            'CANCELLED',
            'COMPLETED'
        ]

        if status_value not in allowed_status:

            return Response(
                {"error": "Invalid status"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            appointment = Appointment.objects.get(
                id=appointment_id,
                is_deleted=False
            )

        except Appointment.DoesNotExist:

            return Response(
                {"error": "Appointment not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        appointment.status = status_value
        appointment.save()

        return Response({
            "message": "Appointment status updated"
        })
# if we are soft deleting then why method type is delete
class SoftDeleteAppointmentView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def delete(self, request, appointment_id):

        try:

            appointment = Appointment.objects.get(
                id=appointment_id,
                is_deleted=False
            )

        except Appointment.DoesNotExist:

            return Response(
                {"error": "Appointment not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        appointment.soft_delete()

        return Response({
            "message": "Appointment soft deleted"
        })

class DoctorAvailableSlotsView(APIView):

    # permission_classes = [IsAuthenticated]

    def get(self, request, doctor_id):

        appointment_date = request.GET.get(
            'appointment_date'
        )
        print("appointment_date----",appointment_date)

        if not appointment_date:

            return Response(
                {
                    "error":
                    "appointment_date is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        appointment_date_obj = datetime.strptime(
            appointment_date,
            "%Y-%m-%d"
        ).date()
        print("appointment_date_obj-----",appointment_date_obj)

        available_slots = get_available_slots(
            doctor_id,
            appointment_date_obj
        )

        return Response({
            "doctor_id": doctor_id,
            "appointment_date": appointment_date,
            "available_slots": available_slots
        })