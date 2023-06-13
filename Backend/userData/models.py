from .deaultValues import *
from django.db import models
from django.contrib.auth.models import AbstractUser,Group , Permission 
from treebeard.mp_tree import MP_Node
from django.contrib.contenttypes.models import ContentType

# Create your models here.


class RoleHierarchy(MP_Node):
      
    #Model representing the role hierarchy.

    #Fields:
        #role: The role name.
        #role_Created: The datetime when the role was created.
        #role_Modified: The datetime when the role was last modified.
        #reporting_role: The reporting role (foreign key to another RoleHierarchy instance).
    
      role = models.CharField(max_length=100 , unique=True)
      role_Created = models.DateTimeField(auto_now_add=True)
      role_Modified = models.DateTimeField(auto_now=True)
      reporting_role = models.ForeignKey("self", blank=True , null=True  , on_delete=models.CASCADE )
      
      def __str__(self):
           return self.role

class Address(models.Model):
    
    #Model representing the address of employees.

    # Fields:
    #     country: The country of the address.
    #     city: The city of the address.
    #     state: The state of the address.
    #     zip_Code: The zip code of the address.
    #     zone: The zone of the address.



    country = models.CharField(max_length=100)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
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
    
    
    name = models.CharField(max_length=240)
    email = models.EmailField(unique=True)
    birthdate = models.DateField(null=True , blank=True)
    phone = models.CharField(max_length=20)
    is_Active = models.BooleanField(default=True)
    joining_Date = models.DateField(blank=True , null=True)
    created_By = models.CharField(max_length=100)
    modified_Person = models.CharField(max_length=200 ,null=True , blank=True)
    role = models.ForeignKey(RoleHierarchy , on_delete=models.PROTECT ,)
    reporting_Person = models.CharField(max_length=200)
    address = models.ForeignKey(Address,on_delete=models.PROTECT  )
    registration_Date = models.DateField(auto_now_add=True,)
    last_Modified = models.DateTimeField(auto_now=True)
    employee_Id = models.CharField(max_length=100,)
    web_User = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name  
    class Meta:  
        verbose_name_plural = "Employees"


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
    
    
    name = models.CharField(max_length=200 ,null=True , blank=True )
    user_permissions = models.ManyToManyField(Permission , related_name="Permited_user")
    email = models.EmailField(unique=True,)
    groups = models.ManyToManyField(Group , related_name="users")
    employee = models.OneToOneField(Employee , on_delete=models.PROTECT  , null=True , blank=True , related_name="user")
    is_Admin = models.BooleanField(default=False)
    USERNAME_FIELD = "username"  
    REQUIRED_FIELDS=["password","email"]
    def __str__(self):
        return self.username
    
    class Meta:  
        verbose_name_plural = "Users"
        

class Admin(AbstractUser):
    
    #   Custom Admin model that extends Django's AbstractUser.

    # Fields:
    #     name: The name of the admin.
    #     user_permissions: The admin's permissions.
    #     join_Count: The join count for the admin.
    #     email: The email of the admin.
    #     groups: The groups the admin belongs to.
    #     is_Admin: Indicates if the user is an admin or not.
    
    # Constants:
    #     USERNAME_FIELD: The field to use as the unique identifier for authentication ( "email").
    #     REQUIRED_FIELDS: The fields required during user creation (set to ["password"]).
    
    
    name = models.CharField(max_length=200 ,null=True , blank=True )
    user_permissions = models.ManyToManyField(Permission , related_name="Permited_Admins")
    join_Count = models.IntegerField(default=default_admin_join_Count)
    email = models.EmailField(unique=True,)
    groups = models.ManyToManyField(Group , related_name="admins")
    is_Admin = models.BooleanField(default=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS=["password"]
    
    def __str__(self):   
        return self.username
    
    class Meta:
        verbose_name_plural = "Admins"
        

    