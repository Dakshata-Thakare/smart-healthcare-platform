from appointments.utils import get_available_slots
from rest_framework import serializers
from .models import Appointment, DoctorAvailability

from rest_framework import serializers
from .models import DoctorAvailability
from datetime import datetime, time


class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailability
        fields = '__all__'

    def validate(self, data):
        start_time = data['start_time']
        end_time = data['end_time']
        doctor = data['doctor']
        weekday = data['weekday']

        if start_time >= end_time:
            raise serializers.ValidationError(
                "End time must be greater than start time"
            )

        existing_slots = DoctorAvailability.objects.filter(
            doctor=doctor,
            weekday=weekday,
            is_available=True
        )
        print("existing_slots: ",existing_slots)

        for slot in existing_slots:

            overlap_exists = (start_time < slot.end_time and end_time > slot.start_time)

            if overlap_exists:
                raise serializers.ValidationError(
                    "Doctor already has overlapping availability slot"
                )

        return data


class DoctorPatientAppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(
        source='patient.username'#Accesses:appointment.patient.username through ORM relationship.
    )

    patient_email = serializers.CharField(source='patient.email')

    class Meta:
        model = Appointment

        fields = [
            'id',
            'patient_name',
            'patient_email',
            'appointment_date',
            'appointment_time',
            'status',
            'reason'
        ]

class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = '__all__'

    def validate(self, data):

        patient = data['patient']
        doctor = data['doctor']
        appointment_date = data['appointment_date']
        appointment_time = data['appointment_time']

        if patient.role != 'PATIENT':
            raise serializers.ValidationError("Selected user is not a patient")

        if doctor.role != 'DOCTOR':
            raise serializers.ValidationError("Selected user is not a doctor")

        available_slots = get_available_slots(
            doctor.id,
            appointment_date
        )

        formatted_time = appointment_time.strftime(
            "%H:%M"
        )

        if formatted_time not in available_slots:

            raise serializers.ValidationError(
                "Selected slot is not available"
            )

        return data