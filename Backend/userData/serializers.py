from rest_framework import serializers
from .models import *



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
        print(role,"this is role")
        my_Adress=Adress.objects.create(city=city,country=country,
            zip_code=zip_code , zone=zone)
        my_Role=RoleHierarchy.objects.get(name=role)
        my_Employee=Employee.objects.create(name=name, email=email,
                                            phone=phone, reporting_Person=reporting_Person,
                                            created_By=created_By,
                                            role=my_Role, Adress=my_Adress)
        
        current_user.save()
        
        return my_Employee
    
class UserSerializer(serializers.ModelSerializer):
       
       class Meta:
           model = user
           fields = ["username","user_permissions","email","groups","password","firstname","lastname"]
       def create(self, validated_data):
           type = self.context.get("type")
           myUser = user if type == "user" else Admin
           createdUser = myUser.objects.create(validated_data)
           createdUser.is_staff = True
           createdUser.is_superuser = True 
           return createdUser  
       
 