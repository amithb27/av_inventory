from rest_framework import serializers
from .models import *
from django.contrib.auth.models import  Permission 
from django.contrib.contenttypes.models import ContentType 
from .deaultValues import default_admin_join_Count
from .ProjectUtilities import makePassword
Employee_Tag ="AV_"

class RoleSerializer(serializers.ModelSerializer):
    
    class Meta :
        model = Role
        fields = ["name","pk"]
    def create(self, validated_data):
        name = validated_data["name"]
        role = Role.objects.create(name= name )
        return role
    #doubt To know 
    def update(self, instance, validated_data):
        instance.name = validated_data["name"]
        instance.save()
        return instance


class RoleHierarchySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleHierarchy
        fields = ("pk",'role',"reporting_role")
                
        # def create(self, validated_data):
            
        #     #Create a RoleHierarchy instance.

        #     #Args:
        #         #validated_data (dict): Validated data containing the role hierarchy information.

        #     #Returns:
        #         #data (dict) : message as a key 
        #     user = self.context.get("user")
        #     role = validated_data["role"]
        #     print(user)
        #     reporting_role = validated_data["reporting_role"]
        #     if reporting_role == "self":
        #          root = RoleHierarchy.add_root(role = role , reporting_role = "self")
        #     else:
        #         try :
        #             parent = RoleHierarchy.objects.get(role = reporting_role)
        #             parent.add_child(role = role , reporting_role = reporting_role)
        #         except Exception as e :
        #             return {"message" : "create reporting role First " , "status":status.HTTP_400_BAD_REQUEST}
        #     user.join_Count -= 1 
        #     return ({"message":"role Created" , "status":status.HTTP_200_OK})

        def update(self,instance, validated_data):
            
            #Update a RoleHierarchy instance.

            #Args:
                #instance: Existing RoleHierarchy instance to be updated.
                #validated_data (dict): Validated data containing the updated role hierarchy information.
 
            #Returns: 
                #None
            instance.reporting_role = validated_data["reporting_role"]
            if instance.reporting_role != "self" :
                parent = RoleHierarchy.objects.get(reporting_role =validated_data.reporting_role )
                instance.move(target = parent, pos="last_child")
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

    class Meta:
        model = Employee 
        fields = ('pk', 'name','email','phone','address',
                  'reporting_Person',"role"
        )
        
    def create(self, validated_data):
               
        #Create an Employee instance.

        #Args:
           # validated_data (dict): Validated data containing the employee information.

        #Returns:
           # tuple: Tuple containing the created employee's primary key and email.
           
        print(validated_data)
        current_user = self.context.get("requestedUser")
        name = validated_data['name']
        email = validated_data['email']
        role = validated_data["role"]
        phone = validated_data['phone']
        reporting_Person = validated_data["reporting_Person"]
        country = validated_data["address"]["country"]
        city = validated_data["address"]["city"]
        zip_code = validated_data["address"]["zip_Code"]
        zone = validated_data["address"]["zone"]
        created_By = current_user.username  
        my_Adress = Address.objects.create(
                                        city=city,
                                        country=country,
                                        zip_Code=zip_code, 
                                        zone=zone
        )
        my_Employee=Employee.objects.create(
                                            name=name,
                                            email=email,
                                            phone=phone,
                                            reporting_Person=reporting_Person,
                                            created_By=created_By,
                                            role=role,
                                            address=my_Adress 
        )
       
        employee_Id = Employee_Tag +str(my_Employee.pk)
        my_Employee.employee_Id = employee_Id
        my_Employee.save()
        return (my_Employee.pk, email)


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
           password = makePassword()
           createdUser = user(email = email ,username = email)
           createdUser.set_password(password)
           createdUser.name = employee.name
           createdUser.employee = employee
           createdUser.is_staff = True
           returned_Object = {
               "email":email,
               "password":password,
               "pk":self.context.get("employee")             
           }
           createdUser.save()
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
           fields = ["email","password","name","username"]
       def create(self, validated_data ):
         
        #Create an Admin instance.

       # Args:
            #validated_data (dict): Validated data containing the admin information.

       # Returns:
           # User: Created User (Admin) instance.
           
           email = validated_data["email"]
           password = validated_data["password"]
           createdAdmin = user(email = email )
           createdAdmin.set_password(password)
           createdAdmin.name =validated_data["name"]
           createdAdmin.username = validated_data["username"]
           createdAdmin.is_Admin = True
           createdAdmin.is_staff = True
           createdAdmin.save() 
           Content_Type = ContentType.objects.filter(app_label = "userData")
           perms = []
           for model in Content_Type :
                perms += list(Permission.objects.filter(content_type = model))
           createdAdmin.user_permissions.set(perms)
           createdAdmin.join_Count = default_admin_join_Count
           createdAdmin.save()
           print(password)
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
           

class NotificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model : Notification
        fields = "__all__"  
              
           
           
        
class ProductSerializer(serializers.ModelSerializer):
    
    class Meta :
        model = Product
        fields = ["pk", "product_Name", "status"]
        
class BrandSerialilzer(serializers.ModelSerializer):
     
    class Meta:
        model = Brand
        fields = ["brand_Name", "status"]

class SizeSeriallizer(serializers.ModelSerializer):

    class Meta:
        model = Size
        fields = ["size_Name", "status"]

class CetegorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Cetegory
        fields = ["cetegory_Name", "status"]

class UnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Unit
        fields = ["unit_name", "status"]