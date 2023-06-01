
from .deaultValues import *
from django.db import models
from django.contrib.auth.models import AbstractUser,Group , Permission 
from treebeard.mp_tree import MP_Node
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
# Create your models here.

class RoleHierarchy(MP_Node):
      role = models.CharField(max_length=100 , unique=True)
      role_Created = models.DateTimeField(auto_now_add=True)
      role_Modified = models.DateTimeField(auto_now=True)
      reporting_role = models.ForeignKey("self", blank=True , null=True  , on_delete=models.CASCADE )
      def __str__(self):
           return self.role
       
class Adress(models.Model):
    ## this model is to store the adress of all employees
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    zip_Code = models.IntegerField()
    zone = models.CharField(max_length=100)
    
    def __str__(self) :
        return self.city
    
    class Meta:
        verbose_name_plural = "Adress"       

class Employee(models.Model):
    ## This creates a model for a Employee
    name = models.CharField(max_length=240)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    last_Modified = models.DateTimeField(auto_now=True)
    created_By = models.CharField(max_length=100)
    role = models.ForeignKey(RoleHierarchy , on_delete=models.PROTECT)
    reporting_Person = models.CharField(max_length=200)
    Adress = models.ForeignKey(Adress,on_delete=models.PROTECT )
    registration_Date = models.DateField(auto_now_add=True,)
    
    def __str__(self):
        return self.name  

class user(AbstractUser):
    user_permissions = models.ManyToManyField(Permission , related_name="Permited_user")
    email = models.EmailField(unique=True,)
    username= models.CharField( max_length=100 ,unique=True)
    groups = models.ManyToManyField(Group , related_name="users")
    USERNAME_FIELD = "username"  
    Employee = models.OneToOneField(Employee , on_delete=models.PROTECT  , null=True , blank=True)
    REQUIRED_FIELDS=["email","password"]
    def __str__(self):
        return self.username
    class Meta:
        verbose_name_plural = "Users"
        

class Admin(AbstractUser):
    user_permissions = models.ManyToManyField(Permission , related_name="Permited_Admins")
    join_Count = models.IntegerField(default=default_admin_join_Count)
    email = models.EmailField(unique=True,)
    username= models.CharField( max_length=100 ,unique=True)
    groups = models.ManyToManyField(Group , related_name="admins")
    Employee = models.OneToOneField(Employee , on_delete=models.PROTECT )
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS=["email","password"]

    def __str__(self):   
        return self.username
    class Meta:
        verbose_name_plural = "Admins"
        
