

from django.db import models
from django.contrib.auth.models import AbstractUser,Group , Permission 
from treebeard.mp_tree import MP_Node
from django.utils import timezone


# Create your models here.
    
    

class user(AbstractUser):
    user_permissions = models.ManyToManyField(Permission , related_name="Permited_user")
    email = models.EmailField(unique=True,)
    username= models.CharField( max_length=100 ,unique=True)
    groups = models.ManyToManyField(Group , related_name="members")
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS=["email","password"]
    def __str__(self):
        return self.username
   
    

        
class RoleHierarchy (MP_Node):
      role = models.CharField(max_length=100 , unique=True)
      role_Created = models.DateTimeField(auto_now_add=True)
      role_Modified = models.DateTimeField(auto_now=True)
      reporting_Role = models.ForeignKey('self',on_delete=models.CASCADE, blank=True , null=True , related_name="children")
      
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
        verbose_name_plural = "Adress Models"
            

    
        
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
    class Meta :
        permissions =[
            ("Add_employee","permission to add an new employee"),
            ("Edit_employee","permission to Edit an new employee"),
            ("Delete_employee","permission to Delete an new employee"),
            ("View_employee","permission to see Details of an new employee"),
        ]