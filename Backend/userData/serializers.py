from rest_framework import serializers
from .models import *


Employee_Tag ="AV_"

class RoleHierarchySerializer(serializers.ModelSerializer):
    # reporting_role = RoleHierarchySerializer
    class Meta:
        model = RoleHierarchy
        fields = ( 'role',"reporting_role")
        
        def create(self, validated_data):
            user = self.context.get("user")
            Group.objects.create(name=validated_data.name)
            root=RoleHierarchy.add_root(role = validated_data.name )
            user.join_Count -= 1 

        def update(self,instance, validated_data):
            instance.role = validated_data.name
            if instance.reporting_role != validated_data.reporting_role :
                parent = RoleHierarchy.objects.get(reporting_role =validated_data.reporting_role )
                instance.move(parent,pos="last_child")
            instance.save()

class AdressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= Address
        fields=("country","city","state","zip_Code","zone")


class EmployeeSerializer(serializers.ModelSerializer):
    role=RoleHierarchySerializer()
    address=AdressSerializer()
    class Meta:
        model = Employee 
        fields = ('pk', 'name','email','role','phone','address',
                  'status','reporting_Person','registration_Date',
                  "created_By",
        )
        
    def create(self, validated_data):
        current_user = self.context.get("requestedUser")
        name=validated_data['name']
        email=validated_data['email']
        role=validated_data['role']['name']
        phone=validated_data['phone']
        reporting_Person=validated_data["reporting_Person"]
        created_By = validated_data["created_By"]
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
           email = validated_data.email
           pk = validated_data.pk
           password = user.objects.make_random_password()
           createdUser = user(email = email )
           createdUser.set_password(password)
           employee = Employee.objects.get(pk=pk)
           createdUser.employee = employee
           createdUser.name = employee.name
           createdUser.save() 
           return createdUser  
       
       def update(self,instance, validated_data):
           instance.set_password(validated_data.password)
           instance.save()
           
           
class AdminSerializer(serializers.ModelSerializer):
       class Meta:
           model = user
           fields = ["email"]
       def create(self, validated_data ):
           email = validated_data.email
           password = validated_data.password
           createdAdmin = user(email = email )
           createdAdmin.set_password(password)
           createdAdmin.name =validated_data.name
           createdAdmin.save() 
           validated_data.user
           return createdAdmin  
       
       def update(self,instance, validated_data):
           instance.set_password(validated_data.password)
           instance.save()
           
       
