from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


# Create your models here.
class Users(AbstractUser):
    ROLE_CHOICES = (
        ('PATIENT','Patient'),
        ('DOCTOR','Doctor'),
        ('ADMIN','Admin'),
        ('RECEPTIONIST','Receptionist')
    )
    role = models.CharField(max_length=20,choices=ROLE_CHOICES,db_index=True)
    phone_number = models.CharField(max_length=15,blank=True,null=True)
    date_of_birth = models.DateField(blank=True,null=True)
    # specialization = models.CharField(max_length=100,blank=True,null=True)
    specialization = models.CharField(max_length=100,blank=True,default="")

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    #Custom model method.Like your own function attached to object.
    # Why Better Than delete()? because delete Physically removes row.
    def soft_delete(self):
        self.is_deleted=True
        self.save()


    def __str__(self):
        return self.username
