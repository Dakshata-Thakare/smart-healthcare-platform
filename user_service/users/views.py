from django.shortcuts import render
from rest_framework import status
from .serializers import RegisterSerializer,DoctorSerializer,PatientSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import (IsAdminOrReceptionist, IsDoctor,IsPatient,IsAdmin,IsReceptionist)
from .models import Users


#Only logged-in users with valid JWT token can access.
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        return Response(
            {
                "username":request.user.username,
                "role":request.user.role,
                "message":"Authenticated successfully"
            }
        )

class RegisterView(APIView):
    #APIView:DRF class-based API view. Handles:HTTP methods,request parsing,authentication,permissions
    def post(self,request):
        serializer = RegisterSerializer(data=request.data) #request.data :Contains JSON request body.
        #serializer does NOT validate yet.It only:creates serializer instance and stores incoming JSON temporarily
        if serializer.is_valid(): #Now DRF performs:required field checks,type validation,choices validation,blank/null validation
            serializer.save() #DRF internally checks:Does create() exist? YES.So DRF calls:create function or calls update()
            return Response({"message":"User registered suceessfully"},status = status.HTTP_201_CREATED)
        return Response({"message":f"Error is {serializer.errors}"},status = status.HTTP_400_BAD_REQUEST)

class DoctorDashboardView(APIView):
    permission_classes = [IsAuthenticated,IsDoctor]
    def get(self,request):
        return Response({"message":"Welcome Doctor"})

class PatientDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsPatient]
    def get(self, request):
        return Response({"message": "Welcome Patient"})

class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    def get(self, request):
        return Response({"message": "Welcome Admin"})

class ReceptionistDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsReceptionist]
    def get(self, request):
        return Response({"message": "Welcome Receptionist"})

class CreateDoctorView(APIView):
    #Permissions check CURRENT LOGGED-IN USERNOT request body username.
    permission_classes = [IsAuthenticated,IsAdmin]
    def post(self,request):
        data = request.data.copy()
        data['role'] ='DOCTOR'
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class DoctorListView(APIView):
    permission_classes = [IsAuthenticated,IsAdminOrReceptionist]
    def get(self,request):
        doctors = Users.objects.filter(role='DOCTOR',is_deleted=False) #this is query set(python object)
        #that's why Serializer Job Convert Python/Django objects --> into JSON-compatible data
        #Without many=True Serializer expects:ONE object
        # With many=True Serializer expects:MULTIPLE objects / QuerySet
        serializer = DoctorSerializer(doctors,many=True)
        return Response(serializer.data)

class UpdateDoctorView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    def put(self, request, doctor_id):
        try:
            doctor = Users.objects.get(id=doctor_id,role='DOCTOR',is_deleted=False)
        except Users.DoesNotExist:
            return Response({"error": "Doctor not found"},status=status.HTTP_404_NOT_FOUND)

        serializer = DoctorSerializer(doctor,data=request.data,partial=True)#partial:Only update provided fields.so serializer will not give error here as remaing fields like username password not send in the req
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

 #here i have doubt if i am doing soft delete then why i have use the method delete   
class SoftDeleteDoctorView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    def delete(self, request, doctor_id):
        try:
            doctor = Users.objects.get(id=doctor_id,role='DOCTOR',is_deleted=False)
        except Users.DoesNotExist:
            return Response({"error": "Doctor not found"},status=status.HTTP_404_NOT_FOUND)

        doctor.soft_delete()
        return Response({"message": "Doctor soft deleted successfully"})

class CreatePatientView(APIView):
    permission_classes = [IsAuthenticated,IsAdminOrReceptionist]
    def post(self, request):
        data = request.data.copy()
        data['role'] = 'PATIENT'
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class PatientListView(APIView):
    permission_classes = [IsAuthenticated,IsAdminOrReceptionist]
    def get(self, request):
        patients = Users.objects.filter(role='PATIENT',is_deleted=False)
        serializer = PatientSerializer(patients,many=True)
        return Response(serializer.data)

class PatientDetailView(APIView):
    permission_classes = [IsAuthenticated,IsAdminOrReceptionist]
    def get(self, request, patient_id):

        try:

            patient = Users.objects.get(
                id=patient_id,
                role='PATIENT',
                is_deleted=False
            )

        except Users.DoesNotExist:

            return Response(
                {"error": "Patient not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PatientSerializer(patient)

        return Response(serializer.data)

class UpdatePatientView(APIView):
    permission_classes = [IsAuthenticated,IsAdminOrReceptionist]
    def put(self, request, patient_id):
        try:
            patient = Users.objects.get(id=patient_id,role='PATIENT',is_deleted=False)
        except Users.DoesNotExist:
            return Response({"error": "Patient not found"},status=status.HTTP_404_NOT_FOUND)

        serializer = PatientSerializer(patient,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#same question if i am doing soft delete why delete method i set??
class SoftDeletePatientView(APIView):

    permission_classes = [IsAuthenticated, IsAdminOrReceptionist]

    def delete(self, request, patient_id):

        try:

            patient = Users.objects.get(
                id=patient_id,
                role='PATIENT',
                is_deleted=False
            )

        except Users.DoesNotExist:

            return Response(
                {"error": "Patient not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        patient.soft_delete()

        return Response({
            "message": "Patient soft deleted successfully"
        })