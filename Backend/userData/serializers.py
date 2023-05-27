from rest_framework import serializers
from .models import *

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ( 'name',)

class RoleHierarchySerializer(serializers.ModelSerializer):
     class Meta:
        model = RoleHierarchy
        fields = ( 'name', 'parent')
     def create(self, validated_data):
         if validated_data.name == validated_data.reportingRole:
             root=RoleHierarchy.add_root(validated_data.name)
             return root
       
         try:
           reportingrole = RoleHierarchy.objects.get(name=validated_data.reportingRole)
           child= RoleHierarchy.add_child(name=validated_data.name,parent=reportingrole)
           return  child
       
         except RoleHierarchy.DoesNotExist:
             root=RoleHierarchy.add_root(validated_data.reportingRole)
             child= RoleHierarchy.add_child(name=validated_data.name , parent=root)
             return  child
         



class AdressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= Adress
        fields=("country","city","state","zip_code","zone")


class EmployeeSerializer(serializers.ModelSerializer):
    role=RoleSerializer()
    Adress=AdressSerializer()
    class Meta:
        model = Employee 
        fields = ('pk', 'name','email','role','phone','Adress',
                  'status','reporting_Person','registration_Date',
                  "created_By",
        )
    def create(self, validated_data):
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
        my_Role=Role.objects.get(name=role)
        my_Employee=Employee.objects.create(name=name, email=email,
                                            phone=phone, reporting_Person=reporting_Person,
                                            created_By=created_By,
                                            role=my_Role, Adress=my_Adress)
        
        return my_Employee