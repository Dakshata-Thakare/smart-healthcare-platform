
from rest_framework import serializers
from .models import Users
class RegisterSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(write_only=True) #write only make sure in response never password shared for best security practice
    class Meta:
        model = Users
        fields = ['username','password','email','role','phone_number','date_of_birth','specialization']
    
    def create(self,validated_data):
        #create_user()----> Automatically:hashes password and secures authentication
        user = Users.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            phone_number=validated_data.get('phone_number'),
            date_of_birth=validated_data.get('date_of_birth'),
            specialization=validated_data.get('specialization','') # did this changes because for patient specialization we dont have so made that field blank true and default empty string and here also default as a empty string as python if the value not get then it takes null that's why previously getting errror
        )
        return user
    
class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users

        fields = [
            'id',
            'username',
            'email',
            'phone_number',
            'specialization',
            'date_of_birth',
            'created_at'
        ]

        read_only_fields = ['created_at']

#Why Separate Serializer?
# Different roles expose different fields.
# Doctor:specialization
# Patient:No specialization needed.
class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users

        fields = [
            'id',
            'username',
            'email',
            'phone_number',
            'date_of_birth',
            'created_at'
        ]

        read_only_fields = ['created_at']
