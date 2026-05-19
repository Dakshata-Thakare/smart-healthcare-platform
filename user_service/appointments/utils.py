from datetime import datetime, timedelta

from appointments.models import Appointment, DoctorAvailability
#Slot Generation Logic
# This function ONLY generates:POSSIBLE slots and NOT available slots.
def generate_time_slots(start_time,end_time,slot_duration=30):
    slots = []
    #Time objects alone cannot be incremented with timedelta easily.
    # So Python converts:09:00 into: 2026-05-15 09:00:00
    current = datetime.combine(
        datetime.today(),
        start_time
    )

    end = datetime.combine(
        datetime.today(),
        end_time
    )

    while current < end:
        slots.append(
            current.time().strftime("%H:%M") #current.time()Extracts only time part.
        )

        current += timedelta(
            minutes=slot_duration
        )
    return slots

def get_available_slots(doctor_id,appointment_date):
        # Convert date into weekday name
        #%A Means : Full weekday name
        #strptime means:String Parse 
        #Convert STRING into datetime object
    weekday = (appointment_date.strftime("%A").upper())
    print("weekday",weekday)
    print("doctor_id",doctor_id)
    availability = DoctorAvailability.objects.filter(doctor_id=doctor_id,weekday=weekday,is_available=True)
    print("availability: ",availability)

    if not availability.exists():
        return []

    all_slots = []

    for slot in availability:
        generated_slots = generate_time_slots(slot.start_time,slot.end_time)
        all_slots.extend(generated_slots)

    booked_slots = Appointment.objects.filter(
        doctor_id=doctor_id,
        appointment_date=appointment_date,
        is_deleted=False
    ).values_list(
        'appointment_time',
        flat=True
    )

    booked_slots = [time.strftime("%H:%M") for time in booked_slots]
    available_slots = [slot for slot in all_slots if slot not in booked_slots]

    return available_slots