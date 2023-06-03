from rest_framework import serializers
from .models import *


Employee_Tag ="AV_"

class RoleHierarchySerializer(serializers.ModelSerializer):
    # reporting_role = RoleHierarchySerializer
    class Meta:
        model = RoleHierarchy
        fields = ( 'role',"reporting_role")
        
        def create(self, validated_data):
            Group.objects.create(name=validated_data.name)
            root=RoleHierarchy.add_root(role = validated_data.name )

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
        current_user.join_Count -= 1    
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
        print(role,"this is role")
        my_Adress=Address.objects.create(city=city,country=country,
            zip_code=zip_code , zone=zone)
        my_Role=RoleHierarchy.objects.get(name=role)
        my_Employee=Employee.objects.create(name=name, email=email,
                                            phone=phone, reporting_Person=reporting_Person,
                                            created_By=created_By,
                                            role=my_Role, Adress=my_Adress ,employee_Id =employee_Id)
        
        current_user.save()
        
        
        return ( my_Employee.pk , email )
    
class UserSerializer(serializers.ModelSerializer):
       class Meta:
           model = user
           fields = ["email",]
       def create(self, validated_data):
           email = validated_data.email
           pk = validated_data.pk
           password = user.objects.make_random_password()
           type = self.context.get("type")
           myUser = Admin if type == "Admin" else user
           createdUser = myUser(email = email )
           createdUser.set_password(password)
           employee = Employee.objects.get(pk=pk)
           createdUser.employee = employee
           
           if type == "Admin" :
                createdUser.is_staff = True
                createdUser.is_superuser = True 
           createdUser.save() 
           return createdUser  
       
       def update(self,instance, validated_data):
           instance.set_password(validated_data.password)
           instance.save()
           
       
