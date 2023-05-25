from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
# Create your models here.

# class UserManager(BaseUserManager):
#     def create_User(self, email, password=None, **extra_fields):
       
#         # Normalize the email address
#         email = self.normalize_email(email)

#         # Create a new user instance
#         user = self.model(email=email, **extra_fields)

#         # Set the password
#         user.set_password(password)

#         # Save the user
#         user.save(using=self._db)
#         return user

#     def create_Superuser(self, email, password=None, **extra_fields):
#         # Create a new superuser with the given email and password
#         user = self.create_User(email, password, **extra_fields)
#         user.is_admin = True
#         user.save(using=self._db)
#         return user
    

# class My_User(AbstractBaseUser):
    
#     first_Name = models.CharField(max_length=100 )
#     last_Name = models.CharField(max_length=100 )
#     email = models.EmailField(unique=True,)
#     password = models.CharField(max_length=128 , )
#     user_Name= models.CharField(editable=False , max_length=100 ,unique=True)
    
#     USERNAME_FIELD = "user_Name"
#     REQUIRED_FIELDS = ['password',"email","first_Name","last_Name"]  

#     objects = UserManager()
    
#     def save(self, *args, **kwargs):
#         self.user_Name = self.first_Name + self.last_Name
#         super().save(*args, **kwargs)
        
class Adress(models.Model):
    ## this model is to store the adress of all employees
        country = models.CharField(max_length=100)
        city = models.CharField(max_length=64)
        state = models.CharField(max_length=64)
        zip_code = models.IntegerField()
        zone = models.CharField(max_length=100)
        
        def __str__(self) :
            return self.city
        
        class Meta:
            verbose_name_plural = "Adress Models"
            
    
    
class Role(models.Model):
    
    #This create a Roles of the employees
    role_Created = models.DateTimeField(auto_now_add=True)
    role_Modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=240)
    class Meta:
        verbose_name_plural = "roles"
    
    def __str__(self):
        return self.name
    
        
class Employee(models.Model):
    
    ## This creates a model for a Employee
    name = models.CharField(max_length=240)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    last_Modified = models.DateTimeField(auto_now=True)
    created_By=models.CharField(max_length=100)
    role = models.ForeignKey(Role , on_delete=models.PROTECT)
    reporting_Person = models.CharField(max_length=200)
    Adress = models.ForeignKey(Adress,on_delete=models.PROTECT )
    registration_Date = models.DateField(auto_now_add=True,)
    # modified_By = models.CharField(max_length=100)
    def __str__(self):
        return self.name 
    