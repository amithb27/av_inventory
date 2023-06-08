from .deaultValues import *
from django.db import models
from django.contrib.auth.models import AbstractUser,Group , Permission 
from treebeard.mp_tree import MP_Node
from django.contrib.contenttypes.models import ContentType

# Create your models here.


class RoleHierarchy(MP_Node):
      role = models.CharField(max_length=100 , unique=True)
      role_Created = models.DateTimeField(auto_now_add=True)
      role_Modified = models.DateTimeField(auto_now=True)
      reporting_role = models.ForeignKey("self", blank=True , null=True  , on_delete=models.CASCADE )
      
      def __str__(self):
           return self.role

class Address(models.Model):
    ## this model is to store the adress of all employees
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
    ## This creates a model for a Employee
    name = models.CharField(max_length=240)
    email = models.EmailField(unique=True)
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
        

    