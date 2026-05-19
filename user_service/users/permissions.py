from rest_framework.permissions import BasePermission

#BasePermission   : Base class for custom authorization logic.
#has_permission() : Runs before API execution.
class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'DOCTOR'


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'PATIENT'


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        print("request: ",request)
        #request.user Means:User extracted from JWT token
        #request.data Means:Incoming API body
        print(request.user.username)
        print(request.user.role)
        return request.user.role == 'ADMIN'


class IsReceptionist(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'RECEPTIONIST'

class IsAdminOrReceptionist(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['ADMIN', 'RECEPTIONIST']

#Doctor Access
# Doctor:id=5
# Appointment:doctor_id=5 allowed
#suppose patient 1 is trying to access the another patient2 appointment details then he is not allowed imp oops concept taught here understand this properly
class CanAccessAppointment(BasePermission):
    def has_object_permission(self,request,view,obj):
        print("object is    ",obj)
        user = request.user
        print("user is ",user)
        print("userrole",user.role)
        if user.role in ['ADMIN', 'RECEPTIONIST']:
            return True
        
        if user.role == 'DOCTOR':
            return obj.doctor == user

        if user.role == 'PATIENT':
            return obj.patient == user

        return False