from .deaultValues import *
from django.db import models
from django.contrib.auth.models import AbstractUser,Group , Permission 
from treebeard.mp_tree import MP_Node
from django.contrib import admin  

# Create your models here.

class AdminClass(admin.ModelAdmin):
    readonly_fields = ("role_Modified","role_Created")

class RoleHierarchy(MP_Node):
      
    #Model representing the role hierarchy.

    #Fields:
        #role: The role name.
        #role_Created: The datetime when the role was created.
        #role_Modified: The datetime when the role was last modified.
        #reporting_role: The reporting role (foreign key to another RoleHierarchy instance).
           
      role = models.CharField(help_text="role_name", max_length=100 , unique=True)
      role_Created = models.DateTimeField(auto_now_add=True)
      role_Modified = models.DateTimeField(auto_now=True)
      reporting_role = models.CharField(max_length=200 )
      
      def __str__(self):
           return self.role
       
class Role(models.Model):
    #Model representing the role 
    
    #Fields:
        #name: name of the role 
    
    name = models.CharField(max_length=200 ,unique=True)
    
    def __str__(self):
        return self.name

class Address(models.Model):
    
    #Model representing the address of employees.

    # Fields:
    #     country : The country of the address.
    #     city : The city of the address.
    #     state : The state of the address.
    #     zip_Code : The zip code of the address.
    #     zone : The zone of the address.
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=64 , blank=True)
    state = models.CharField(max_length=64 )
    zip_Code = models.IntegerField()
    zone = models.CharField(max_length=100)
    
    def __str__(self) :
        return self.city
    
    class Meta:
        verbose_name_plural = "addresses"       

class Employee(models.Model):
    
    # Model representing an Employee.

    # Fields:
    #     name: The name of the employee.
    #     email: The email of the employee.
    #     birthdate: The birthdate of the employee.
    #     phone: The phone number of the employee.
    #     is_Active: Indicates if the employee is active or not.
    #     joining_Date: The date when the employee joined.
    #     created_By: The person who created the employee.
    #     modified_Person: The person who last modified the employee.
    #     role: The role hierarchy of the employee (foreign key to RoleHierarchy).
    #     reporting_Person: The person who the employee reports to.
    #     address: The address of the employee (foreign key to Address).
    #     registration_Date: The date when the employee was registered.
    #     last_Modified: The datetime when the employee was last modified.
    #     employee_Id: The ID of the employee.
    #     web_User: Indicates if the employee is a web user or not.
    # first_Name =  models.CharField(max_length=240 )
    # middle_Name =  models.CharField(max_length=240 , null= True , blank= True)
    # last_Name =  models.CharField(max_length=240 , null= True , blank= True)
    name = models.CharField(max_length=240 , null= True , blank= True)
    email = models.EmailField(unique=True)
    birthdate = models.DateField(null=True , blank=True)
    phone = models.CharField(max_length=20)
    is_Active = models.BooleanField(default=True)
    joining_Date = models.DateField(blank=True , null=True)
    created_By = models.CharField(max_length=100)
    modified_Person = models.CharField(max_length=200 ,null=True , blank=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT ,)
    reporting_Person = models.CharField(max_length=200)
    address = models.ForeignKey(Address,on_delete=models.PROTECT  )
    registration_Date = models.DateField(auto_now_add=True)
    last_Modified = models.DateTimeField(auto_now=True)
    employee_Id = models.CharField(max_length=100,)
    web_User = models.BooleanField(default=False ) 
    
    def __str__(self):
        return self.name  
    
    class Meta:  
        verbose_name_plural = "Employees"

class Notification(models.Model):
    messageCode = models.CharField(max_length=10)
    message = models.CharField(max_length=20)
    addTime = models.DateTimeField(auto_now_add=True)
    readTime = models.DateTimeField(auto_now =True)
    
    def __str__(self) -> str:
        return self.messageCode

class user(AbstractUser):

    
    #   Custom User model that extends Django's AbstractUser.

    # Fields:
    #     name: The name of the user.
    #     user_permissions: The user's permissions.
    #     email: The email of the user.
    #     groups: The groups the user belongs to.
    #     employee: The related Employee instance (one-to-one relationship).
    #     is_Admin: Indicates if the user is an admin or not.
    
    # Constants:
    #     USERNAME_FIELD: The field to use as the unique identifier for authentication ( "username").
    #     REQUIRED_FIELDS: The fields required during user creation (["password", "email"]).
    
    username = models.CharField(unique= True , max_length=200)
    name = models.CharField(max_length=200 ,null=True , blank=True )
    user_permissions = models.ManyToManyField(Permission , related_name="Permited_user"  ,blank=True)
    email = models.EmailField(unique=True,)
    groups = models.ManyToManyField(Group , related_name="users")
    employee = models.OneToOneField(Employee , on_delete=models.PROTECT  , null=True , blank=True , related_name="user")
    is_Admin = models.BooleanField(default=False)
    join_Count = models.IntegerField(null=True , blank=True)
    USERNAME_FIELD = "username"  
    REQUIRED_FIELDS=["password","email"]
    notifications = models.ManyToManyField(Notification , related_name="user")
    def __str__(self):
        return self.username
    
    class Meta:  
        verbose_name_plural = "Users"
 
# class Customer_Client_Details(models.Model):
#     ## This creates a model for a Client_Details
#     customer_Name = models.CharField(max_length=100)
#     website = models.TextField(max_length=200)
#     reference = models.TextField(max_length=200)
#     description = models.TextField(max_length=200)
#     phone_Number = models.IntegerField()
#     landline_Number = models.IntegerField()
#     pan_Number = models.CharField(max_length=100)
    
#     def __str__(self):
#         return self.customer_Name       

# class Customer_Billing_Details(models.Model):
    
#     ## This creates a model for a Billing_Details
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

# class Customer_Shipping_Address(models.Model):
    
#     ## This creates a model for a Shipping_Address
#     address = models.CharField(max_length=100)
#     zone = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     city = models.CharField(max_length=100)
#     pin_Code = models.IntegerField()
#     sales_Person = models.CharField(max_length=100)
    
  
#     def __str__(self):
#         return self.name  

class Company_Details(models.Model):
      company_Name =  models.CharField(max_length=100)
      landline =  models.CharField(max_length=100)
      mobile =  models.CharField(max_length=100)
      email =  models.CharField(max_length=100)
    #  customer_type = models.ForeignKey(Customer_Type, on_delete=models.PROTECT)
      special_Remarks = models.CharField(max_length=100)
      sales_Person  = models.ForeignKey(Employee, on_delete=models.PROTECT)

class Contact_Details(models.Model):
      contact_Name =  models.CharField(max_length=100)
      landline =  models.CharField(max_length=100)
      mobile =  models.CharField(max_length=100)
      email =  models.CharField(max_length=100)

class Customer(models.Model):
        ## This creates a model for a Customer
     company_Details = models.ForeignKey(Company_Details , on_delete=models.CASCADE)
     contact_Details =  models.ForeignKey(Contact_Details , on_delete=models.CASCADE)
     adress_Details = models.ForeignKey(Address , on_delete=models.CASCADE)
     def __str__(self) :
          return  self.customer_Id  
      
class Inventory_Master(models.Model):
    
    ware_House_Code = models.CharField(max_length=10)
    ware_House_Name = models.CharField(max_length=20)
    location_1 = models.TextField()
    Zone = models.CharField( max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode  = models.CharField(max_length=100)
    min_Qty = models.CharField( max_length=100)
    max_Qty = models.CharField( max_length=100)  


















