from rest_framework import serializers
from .models import *
from rest_framework import status 
Employee_Tag ="AV_"


class RoleSerializer(serializers.ModelSerializer):
    
    class Meta :
        model = Role
        fields = ["name"]
    def create(self, validated_data):
        name = validated_data["name"]
        role = Role.objects.create(name= name )
        return role
    def update(self, instance, validated_data):
        instance.name = validated_data["name"]
        instance.save()
        return instance


class RoleHierarchySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleHierarchy
        fields = ('role',"reporting_role")
        
        def create(self, validated_data):
            
            #Create a RoleHierarchy instance.

            #Args:
                #validated_data (dict): Validated data containing the role hierarchy information.

            #Returns:
                #data (dict) : message as a key 
            
            user = self.context.get("user")
            role = validated_data.role
            reporting_role = validated_data.reporting_role
            # Group.objects.create(name=validated_data.name )
            if reporting_role == "self":
                 root = RoleHierarchy.add_root(role = role , reporting_role = "self")
            else:
                try :
                    parent = RoleHierarchy.objects.get(role = reporting_role)
                    parent.add_child(role = role , reporting_role = reporting_role)
                except Exception as e :
                    return {"message" : "create reporting role First " , "status":status.HTTP_400_BAD_REQUEST}
            user.join_Count -= 1 
            return ({"message":"role Created" , "status":status.HTTP_200_OK})

        def update(self,instance, validated_data):
            
            #Update a RoleHierarchy instance.

            #Args:
                #instance: Existing RoleHierarchy instance to be updated.
                #validated_data (dict): Validated data containing the updated role hierarchy information.
 
            #Returns: 
                #None
            
            instance.role = validated_data.role
            instance.reporting_role = validated_data.reporting_role
            if instance.reporting_role != "self" :
                parent = RoleHierarchy.objects.get(reporting_role =validated_data.reporting_role )
                instance.move(parent,pos="last_child")
            else :
                instance.move(target = None)
            instance.save()
            return  ({"message":"role Updated"})
            

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
    address=AdressSerializer()
    class Meta:
        model = Employee 
        fields = ('pk', 'name','email','phone','address',
                  'reporting_Person',"role","employee_Id"
        )
        
    def create(self, validated_data):
               
        #Create an Employee instance.

        #Args:
           # validated_data (dict): Validated data containing the employee information.

        #Returns:
           # tuple: Tuple containing the created employee's primary key and email.
           
        print(validated_data)
        current_user = self.context.get("requestedUser")
        name=validated_data['name']
        email=validated_data['email']
        role=validated_data["role"]
        phone=validated_data['phone']
        reporting_Person=validated_data["reporting_Person"]
        country=validated_data["address"]["country"]
        city = validated_data["address"]["city"]
        zip_code=validated_data["address"]["zip_Code"]
        zone=validated_data["address"]["zone"]
        created_By = current_user.username  
        my_Adress=Address.objects.create(city=city,country=country,
            zip_Code=zip_code , zone=zone)
        
        my_Employee=Employee.objects.create(name=name, email=email,
                                            phone=phone, reporting_Person=reporting_Person,
                                            created_By=created_By,
                                            role=role, address=my_Adress ,employee_Id =employee_Id)
        employee_Id = Employee_Tag + my_Employee.pk
        return ( my_Employee.pk , email )
    
class UserSerializer(serializers.ModelSerializer):
       class Meta:
           model = user
           fields = ["email","employee"]
       def create(self, validated_data):
            #Create a user with a random password.

            #Args:
                #validated_data (dict): Validated data containing the user information.

            #Returns:
                #dict: Dictionary containing the created user's email, password, and pk.
              
           email = validated_data["email"]
           employee = validated_data["employee"]
           password = user.objects.make_random_password()
           createdUser = user(email = email ,username = email)
           createdUser.set_password(password)
           createdUser.name = employee.name
           createdUser.save() 
           returned_Object = {
               "email":email,
               "password":password,
               "pk":self.context.get("employee")             
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
