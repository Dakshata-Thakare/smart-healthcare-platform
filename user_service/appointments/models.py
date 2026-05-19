from django.db import models
from django.db.models import Q
from users.models import Users
# Create your models here.
class Appointment(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    )
    patient = models.ForeignKey(
        Users,
        on_delete=models.PROTECT, #appointments are critical records and prevent accidental hard deletion
        related_name='patient_appointments'   ,
        limit_choices_to={'role': 'PATIENT'}#patient field only accepts PATIENT users

    )
    doctor = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        null=True,blank=True,
        related_name='doctor_appointments',
        limit_choices_to={'role': 'DOCTOR'} #doctor field only accepts DOCTOR users

    )
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        patient_name  = self.patient.username if self.patient else "Deleted Patient"
        doctor_name  = self.doctor.username if self.doctor else "Deleted Doctor"
        return (
            f"{patient_name} -> "
            f"{doctor_name} | "
            f"{self.appointment_date} "
            f"{self.appointment_time}"
        )    
    def soft_delete(self):
        self.is_deleted = True
        self.save()

    #prevents Two patients booking same doctor slot
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['doctor','appointment_date','appointment_time'],
                condition = Q(is_deleted=False),
                name  ='unique_active_doctor_slot'
            )
        ]
class DoctorAvailability(models.Model):
    WEEKDAYS = (
        ('MONDAY', 'Monday'),
        ('TUESDAY', 'Tuesday'),
        ('WEDNESDAY', 'Wednesday'),
        ('THURSDAY', 'Thursday'),
        ('FRIDAY', 'Friday'),
        ('SATURDAY', 'Saturday'),
        ('SUNDAY', 'Sunday'),
    )
    
    doctor = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='availabilities',limit_choices_to={'role':'DOCTOR'})
    print("doctor is ",doctor)

    weekday = models.CharField(max_length=20,choices=WEEKDAYS)
    print()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
            fields=['doctor','weekday','start_time'],
            name='unique_doctor_weekday_slot'
            )
        ]

    def __str__(self):
        return f"{self.doctor.username} | {self.weekday} | {self.start_time}"