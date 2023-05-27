
from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser,Group , Permission 
from treebeard.mp_tree import MP_Node
from django.utils import timezone


# Create your models here.

# class Profile(models.Model):
  
#     dateOfBirth = models.DateField(null=True , blank=True , default=timezone.now)
    
#     age = models.IntegerField(null=True , blank=True ,default=1)
    
    
    
    
   
    
    
    

class user(AbstractUser):
    # profile = models.OneToOneField(Profile , on_delete=models.CASCADE)
    user_permissions = models.ManyToManyField(Permission , related_name="Permited_user")
    email = models.EmailField(unique=True,)
    username= models.CharField( max_length=100 ,unique=True)
    is_active = models.BooleanField(default=True)
    # is_admin = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group , related_name="members")
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS=["email","password","username"]
    def __str__(self):
        return self.username
   
    

        
class RoleHierarchy (MP_Node):
      name = models.CharField(max_length=100 , unique=True)
      
      parent = models.ForeignKey('self',on_delete=models.CASCADE, blank=True , null=True , related_name="children")
      
      def __str__(self):
           return self.name
         
        
# class Client_Details(models.Model):
#     ## This creates a model for a Client_Details
#     customer_Name = models.CharField(max_length=100)
#     website = models.TextField()
#     reference = models.TextField()
#     description = models.TextField()
#     phone_Number = models.IntegerField()
#     landline_Number = models.IntegerField()
#     pan_Number = models.CharField(max_length=100)
#     is_Active = models.BooleanField(default=True)
    
#     def __str__(self):
#         return self.customer_Name
         
# class contact_Details(models.Model):
    
#     ## This creates a model for a contact_Details
#     customer_Name = models.CharField(max_length=100)
#     contact_Person = models.CharField(max_length=100)
#     mobile_Number = models.IntegerField()
#     alternate_Mobile_Number = models.IntegerField()
#     emailId = models.EmailField()
#     designation = models.CharField(max_length=100)

#     def __str__(self):
#         return self.customer_Name  

# class Billing_Details(models.Model):
    
#     ## This creates a model for a Billing_Details
#     address = models.TextField()
#     zone = models.CharField(max_length=100) 
#     country = models.CharField(max_length=100) 
#     state = models.CharField(max_length=100) 
#     city = models.CharField(max_length=100) 
#     pin_Code = models.IntegerField() 
#     billing_Name = models.CharField(max_length=100) 
#     billing_GSTIN = models.CharField(max_length=100) 
#     pAN_Number = models.CharField(max_length=100) 
#     udyog_Aadhar = models.IntegerField() 
#     export_No = models.CharField(max_length=100) 

#     def __str__(self):
#         return self.country 
    
    
    
    
    
# class Shipping_Address(models.Model):
    
#     ## This creates a model for a Shipping_Address
#     address = models.CharField(max_length=100)
#     zone = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     city = models.CharField(max_length=100)
#     pin_Code = models.IntegerField()
#     sales_Person = models.CharField(max_length=100)
    
  
#     def __str__(self):
#         return self.name  

    
     

# class Customer(models.Model):
#         ## This creates a model for a Customer
#       customer_Id  =  models.CharField(max_length=100)
#       client_Details  = models.ForeignKey(Client_Details , on_delete=models.PROTECT)
#       billing_Details = models.ForeignKey(Billing_Details , on_delete=models.PROTECT)
#       shipping_Address = models.ForeignKey(Shipping_Address , on_delete=models.PROTECT)
        
#       def __str__(self) :
#           return  self.customer_Id

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
    def __str__(self):
        return self.name 
    