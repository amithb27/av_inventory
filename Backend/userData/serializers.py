from rest_framework import serializers
from .models import *

Employee_Tag ="AV_"

class RoleHierarchySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleHierarchy
        fields = ( 'role',"reporting_role")
        
        def create(self, validated_data):
            
            #Create a RoleHierarchy instance.

            #Args:
                #validated_data (dict): Validated data containing the role hierarchy information.

            #Returns:
                #None
                
            user = self.context.get("user")
            Group.objects.create(name=validated_data.name)
            root=RoleHierarchy.add_root(role = validated_data.name )
            user.join_Count -= 1 

        def update(self,instance, validated_data):
            
            #Update a RoleHierarchy instance.

            #Args:
                #instance: Existing RoleHierarchy instance to be updated.
                #validated_data (dict): Validated data containing the updated role hierarchy information.

            #Returns:
                #None
                
            instance.role = validated_data.name
            if instance.reporting_role != validated_data.reporting_role :
                parent = RoleHierarchy.objects.get(reporting_role =validated_data.reporting_role )
                instance.move(parent,pos="last_child")
            instance.save()

class AdressSerializer(serializers.ModelSerializer):
    #serializes The Adress model
    class Meta:
        model= Address
        fields=("country","city","state","zip_Code","zone")


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Employee model.

    Attributes:
        role: Serializer field for the role hierarchy.
        address: Serializer field for the address.
    """
    role=RoleHierarchySerializer()
    address=AdressSerializer()
    class Meta:
        model = Employee 
        fields = ('pk', 'name','email','role','phone','address',
                  'status','reporting_Person','registration_Date',
                  "created_By",
        )

    def create(self, validated_data):
               
        #Create an Employee instance.

        #Args:
           # validated_data (dict): Validated data containing the employee information.

        #Returns:
           # tuple: Tuple containing the created employee's primary key and email.
        
        current_user = self.context.get("requestedUser")
        name=validated_data['name']
        email=validated_data['email']
        role=validated_data['role']['name']
        phone=validated_data['phone']
        reporting_Person=validated_data["reporting_Person"]
        # created_By = validated_data["created_By"]
        country=validated_data["Adress"]["country"]
        city = validated_data["Adress"]["city"]
        zip_code=validated_data["Adress"]["zip_code"]
        zone=validated_data["Adress"]["zone"]
        employee_Id = Employee_Tag + str(validated_data.pk)
        created_By = current_user.name  
        my_Adress=Address.objects.create(city=city,country=country,
            zip_code=zip_code , zone=zone)
        my_Role=RoleHierarchy.objects.get(name=role)
        my_Employee=Employee.objects.create(name=name, email=email,
                                            phone=phone, reporting_Person=reporting_Person,
                                            created_By=created_By,
                                            role=my_Role, Adress=my_Adress ,employee_Id =employee_Id)
        return ( my_Employee.pk , email )
    
class UserSerializer(serializers.ModelSerializer):
       class Meta:
           model = user
           fields = ["email",]
       def create(self, validated_data):
            #Create a user with a random password.

            #Args:
                #validated_data (dict): Validated data containing the user information.

            #Returns:
                #dict: Dictionary containing the created user's email, password, and pk.
                
           email = validated_data.email
           pk = validated_data.pk
           password = user.objects.make_random_password()
           createdUser = user(email = email )
           createdUser.set_password(password)
           employee = Employee.objects.get(pk=pk)
           createdUser.employee = employee
           createdUser.name = employee.name
           createdUser.save() 
           returned_Object = {
               "email":email,
               "password":password,
               "pk":pk               
           }
           return returned_Object  
       
       def update(self,instance, validated_data):
           instance.set_password(validated_data.password)
           instance.save()
           
           
class AdminSerializer(serializers.ModelSerializer):
    
    #Serializer for the Admin model.

    #Fields:
       # email: The email field of the admin.
        
       class Meta:
           model = user
           fields = ["email"]
       def create(self, validated_data ):
         
        #Create an Admin instance.

       # Args:
            #validated_data (dict): Validated data containing the admin information.

       # Returns:
           # User: Created User (Admin) instance.
           
           email = validated_data.email
           password = validated_data.password
           createdAdmin = user(email = email )
           createdAdmin.set_password(password)
           createdAdmin.name =validated_data.name
           createdAdmin.is_staff = True
           createdAdmin.is_superuser = True
           createdAdmin.save() 
           validated_data.user
           return createdAdmin  
       
       def update(self,instance, validated_data):   
        
        #Update the admin's password.

        #Args:
            #instance: Existing User (Admin) instance to be updated.
            #validated_data (dict): Validated data containing the updated password.

        #Returns:
            #User: Updated User (Admin) instance.
            
           instance.set_password(validated_data.password)
           instance.save()
