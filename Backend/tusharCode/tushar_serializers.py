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
    


class countrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"

class stateSerializer(serializers.ModelSerializer):
    class Meta:
        model =  State
        fields = "__all__"
    
class citySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields =  "__all__"

class pincodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pincode
        fields = "__all__"

class zoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields =  "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields =  "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields =  "__all__"


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = "__all__"


class CetegorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cetegory
        fields = "__all__"


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        models = Item
        fields = "__all__"



class Item_StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item_Status
        fields = "__all__"


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = "__all__"


class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = "__all__"


class FinishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finish
        fields = "__all__"


class ConceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concept
        fields = "__all__"


class Punch_NameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Punch_Name
        fields = "__all__"


class Order_TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_Type
        fields = "__all__"


class Order_age_completionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_age_completion
        fields = "__all__"


class Order_MethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_Method
        fields = "__all__"


class Production_StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Production_Status
        fields = "__all__"


class Planning_StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planning_Status
        fields = "__all__"


class ManageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Manage
        fields = "__all__"

    # def create(self, validated_data):
    #     design_Code = validated_data['design_Code']
    #     product = validated_data['brand']
    #     size = validated_data['size']
    #     category = validated_data['category']
    #     finish = validated_data['finish']
    #     series = validated_data['series']
    #     grade = validated_data['grade']
    #     design_Name = validated_data['design_Name']
    #     base_Design_Name = validated_data['base_Design_Name']
    #     weight = validated_data['weight']
    #     min_Order_Name = validated_data['min_Order_Name']


    #     return super().create(validated_data)
    
class Inventory_MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory_Master
        fields = "__all__"


class sales_order_creationSerializer(serializers.ModelSerializer):
    class Meta:
        model = sales_order_creation
        fields = "__all__"


class order_Design_AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = order_Design_Analysis
        fields = "__all__"


class Current_StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Current_Stock
        fields = "__all__"


class Current_StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Current_Stock
        fields = "__all__"



class Stock_inSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock_in
        fields = "__all__"


class Stock_OutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock_Out
        fields = "__all__"


class Service_ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_Module
        fields = "__all__"


class Performa_InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performa_Invoice
        fields = "__all__"


class Performa_InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performa_Invoice
        fields = "__all__"


class Planning_For_ClassifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planning_For_Classified
        fields = "__all__"

