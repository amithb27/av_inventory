
from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser,Group , Permission 
from treebeard.mp_tree import MP_Node
from django.utils import timezone


# Create your models here.

class Profile(models.Model):
  
    dateOfBirth = models.DateField(null=True , blank=True , default=timezone.now)
    
    age = models.IntegerField(null=True , blank=True ,default=1)
    
    
class user(AbstractUser):
    profile = models.OneToOneField(Profile , on_delete=models.CASCADE)
    user_permissions = models.ManyToManyField(Permission , related_name="Permited_user")
    email = models.EmailField(unique=True,)
    username= models.CharField( max_length=100 ,unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group , related_name="members")
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS=["email","password","username"]
    def __str__(self):
        return self.username
   
    

        
class RoleHierarchy (MP_Node):
      name = models.CharField(max_length=100 , unique=True)
      
      parent = models.ForeignKey('self',on_delete=models.CASCADE, blank=True , null=True , related_name="children")
      
      def __str__(self):
           return self.name
         
        
class Client_Details(models.Model):
    ## This creates a model for a Client_Details
    customer_Name = models.CharField(max_length=100)
    website = models.TextField()
    reference = models.TextField()
    description = models.TextField()
    phone_Number = models.IntegerField()
    landline_Number = models.IntegerField()
    pan_Number = models.CharField(max_length=100)
    is_Active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.customer_Name


class contact_Details(models.Model):
    
    ## This creates a model for a contact_Details
    customer_Name = models.CharField(max_length=100)
    contact_Person = models.CharField(max_length=100)
    mobile_Number = models.IntegerField()
    alternate_Mobile_Number = models.IntegerField()
    emailId = models.EmailField()
    designation = models.CharField(max_length=100)

    def __str__(self):
        return self.customer_Name  

class Billing_Details(models.Model):
    
    ## This creates a model for a Billing_Details
    address = models.TextField()
    zone = models.CharField(max_length=100) 
    country = models.CharField(max_length=100) 
    state = models.CharField(max_length=100) 
    city = models.CharField(max_length=100) 
    pin_Code = models.IntegerField() 
    billing_Name = models.CharField(max_length=100) 
    billing_GSTIN = models.CharField(max_length=100) 
    pAN_Number = models.CharField(max_length=100) 
    udyog_Aadhar = models.IntegerField() 
    export_No = models.CharField(max_length=100) 

    def __str__(self):
        return self.country 


class Shipping_Address(models.Model):
    
    ## This creates a model for a Shipping_Address
    address = models.CharField(max_length=100)
    zone = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pin_Code = models.IntegerField()
    sales_Person = models.CharField(max_length=100)
    
  
    def __str__(self):
        return self.name  

    
     

class Customer(models.Model):
        ## This creates a model for a Customer
      customer_Id  =  models.CharField(max_length=100)
      client_Details  = models.ForeignKey(Client_Details , on_delete=models.PROTECT)
      billing_Details = models.ForeignKey(Billing_Details , on_delete=models.PROTECT)
      shipping_Address = models.ForeignKey(Shipping_Address , on_delete=models.PROTECT)
        
      def __str__(self) :
          return  self.customer_Id

class Adress(models.Model):
    ## this model is to store the adress of all employees
        country = models.CharField(max_length=100)
        city = models.CharField(max_length=64)
        state = models.CharField(max_length=64)
        zip_code = models.IntegerField()
        zone = models.CharField(max_length=100)
        
        def __str__(self) :
            return self.city
        
        class Meta:
            verbose_name_plural = "Adress Models"
            
    
    
class Role(models.Model):
    
    #This create a Roles of the employees
    role_Created = models.DateTimeField(auto_now_add=True)
    role_Modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=240)
    class Meta:
        verbose_name_plural = "roles"
    
    def __str__(self):
        return self.name
    
        
class Employee(models.Model): 
    ## This creates a model for a Employee
    name = models.CharField(max_length=240)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    last_Modified = models.DateTimeField(auto_now=True)
    created_By=models.CharField(max_length=100)
    role = models.ForeignKey(Role , on_delete=models.PROTECT)
    reporting_Person = models.CharField(max_length=200)
    adress = models.ForeignKey(Adress,on_delete=models.PROTECT )
    registration_Date = models.DateField(auto_now_add=True,)
    def __str__(self):
        return self.name 


class Country(models.Model):
    country_Name = models.CharField(max_length=20)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.country_Name


class State(models.Model):
    country_Name = models.ForeignKey(Country, on_delete=models.PROTECT)
    state = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.state


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    state = models.ForeignKey(State, on_delete=models.PROTECT)
    city_Name = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.city_Name


class Pincode(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    state = models.ForeignKey(State, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    pincode = models.IntegerField()
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.pincode

class Zone(models.Model):
    country_name = models.ForeignKey(Country, on_delete=models.PROTECT) 
    state = models.ForeignKey(State, on_delete=models.PROTECT)
    zone_Name = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.zone_Name

class Product(models.Model):
    product_Name = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.product_Name

class Brand(models.Model):
    brand_Name = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.brand_Name

class Size(models.Model):
    size_Name = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.size_Name

class Cetegory(models.Model):
    cetegory_Name = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.cetegory_Name


class Unit(models.Model):
    unit_Name = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.unit_Name


class Item(models.Model):
    item_Name = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.item_Name


class Item_Status(models.Model):
    item_Status_Name = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return self.item_Status_Name


class Grade(models.Model):
    grad_Name = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return self.grad_Name


class Series(models.Model):
    series_Name = models.CharField(max_length=20)
    status = models.BooleanField()

    def __str__(self):
        return self.series_Name


class Finish(models.Model):
    finish_Name = models.CharField(max_length=20)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.finish_Name


class Concept(models.Model):
    finish_Name = models.ForeignKey(Finish, on_delete=models.PROTECT)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.finish_Name


class Punch_Name(models.Model):
    punch_Name = models.CharField(max_length=20)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.punch_Name


class Order_Type(models.Model):
    order_Name = models.TextField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.order_Name


class Order_Status(models.Model):
    order_Status_Name = models.CharField(max_length=20)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.order_Status_Name


class Order_age_completion(models.Model):   
    order_age_completion_Name =  models.CharField(max_length=20)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.order_age_completion_Name


class Order_Method(models.Model):
    order_Method_Name = models.CharField(max_length=20)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.order_Method_Name


class Production_Status(models.Model):
    production_Status_Name = models.CharField(max_length=20)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.production_Status_Name


class Planning_Status(models.Model):
    Planning_Status_Name = models.CharField(max_length=20)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.Planning_Status_Name


class Manage(models.Model):
    design_Code = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.
    PROTECT)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    size = models.ForeignKey(Size, on_delete=models.PROTECT)
    cetegory = models.ForeignKey(Cetegory, on_delete=models.PROTECT)
    finish = models.ForeignKey(Finish, on_delete=models.PROTECT)
    series = models.ForeignKey(Series, on_delete=models.PROTECT)
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
    design_Name = models.CharField(max_length=20)  # Primary-key
    base_Design_Name = models.TextField()
    weight = models.DecimalField(10,2)
    min_Order_Qty = models.IntegerField()
    max
    product_Pic_Upload = models.ImageField()  # Image field
    remarks = models.TextField()
    puch = models.ForeignKey(Punch_Name, on_delete=models.PROTECT)
    design_Type = models.TextField()
    design_Status = models.TextField()
    weight = models.TextField()
    min_Qty = models.TextField()
    max_Qty = models.TextField()
    concept_Name = models.TextField()
    concept = models.ForeignKey(Concept, on_delete=models.PROTECT)

    def __str__(self):
        return self.design_Name
    

class Inventory_Master(models.Model):
    ware_House_Code = models.CharField(max_length=10)
    ware_House_Name = models.CharField(max_length=20)
    location_1 = models.TextField()
    Zone = models.ForeignKey(Zone, on_delete=models.PROTECT)
    state = models.ForeignKey(State, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    pincode = models.ForeignKey(Pincode, on_delete=models.PROTECT)
    min_Qty = models.TextField()
    max_Qty = models.TextField()


class sales_order_creation(models.Model):
    order_Id = models.CharField(max_length=20)
    order_Data = models.DateTimeField(auto_now=True)
    cutomer_name = models.CharField(max_length=20)
    billing_Address_line_1 = models.TextField()
    zone_State = models.CharField(max_length=10)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    pincode = models.IntegerField()
    contact_Name = models.TextField()
    contact_Phone = models.CharField(max_length=20)
    order_Type = models.CharField(max_length=20)
    order_Status = models.CharField(max_length=20)
    order_Method = models.CharField(max_length=20)
    remarks = models.TextField()
    add_Order_line_item = models.CharField(max_length=20)
    seq_No = models.CharField(max_length=20)
    ware_House_Name = models.CharField(max_length=20)
    design_Name = models.CharField(max_length=20)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    size = models.ForeignKey(Size, on_delete=models.PROTECT)
    category = models.ForeignKey(Cetegory, on_delete=models.PROTECT)
    finish = models.ForeignKey(Finish, on_delete=models.PROTECT)
    series = models.ForeignKey(Series, on_delete=models.PROTECT)
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
    base_Design_Name = models.CharField(max_length=20)
    weight = models.CharField(max_length=20)
    product_Pic_Upload = models.ImageField()
    design_Type = models.CharField(max_length=20)
    design_status = models.BooleanField(default=True)
    machine = models.CharField(max_length=20)
    weight2 = models.CharField(max_length=20)
    finish2 = models.CharField(max_length=20)
    concept_Name = models.CharField(max_length=20)
    concept = models.ForeignKey(Concept, on_delete=models.PROTECT)
    # total_Opening_Stock =                                 ################
    Min_oreder_Qty = models.CharField(max_length=20)
    oreder_Qty = models.CharField(max_length=20)
    pcs = models.CharField(max_length=20)
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
    batch = models.CharField(max_length=20)
    pack_brand = models.CharField(max_length=20)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    order_Qty = models.CharField(max_length=20)
    oc_Remarks = models.TextField()
    B_Weights =  models.TextField()
    shade = models.CharField(max_length=20)
    shipping_Address = models.ForeignKey(Shipping_Address, on_delete=models.PROTECT)
    location_1 = models.TextField()
    state = models.ForeignKey(State, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    pin_code = models.ForeignKey(Pincode, on_delete=models.PROTECT)
    # total_weight =                                            ###############
    # Current_Stock =                                           ###############


class order_Design_Analysis(models.Model):
    created_Data = models.DateField()
    deisgn_analysis_id = models.CharField(max_length=20)
    seq_No = models.CharField(max_length=10)
    design_Name = models.CharField(max_length=20)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    size =  models.ForeignKey(Size, on_delete=models.PROTECT)
    category = models.ForeignKey(Cetegory, on_delete=models.PROTECT)
    finish = models.ForeignKey(Finish, on_delete=models.PROTECT)
    series = models.ForeignKey(Series, on_delete=models.PROTECT)
    # pre =                                                 #############
    # std =                                                   #############
    # com =                                                    #############
    # eco =                                                     #############
    total_Qty = models.CharField(max_length=20)
    base_Design_Name = models.CharField(max_length=20)
    weight = models.CharField(max_length=20)
    product_Pic_Upload = models.ImageField()
    desing_Type = models.CharField(max_length=20)
    desing_Status = models.CharField(max_length=20)
    machine = models.CharField(max_length=20)
    weight2 = models.CharField(max_length=20)
    concept_Name = models.CharField(max_length=20)
    concept = models.ForeignKey(Concept, on_delete=models.PROTECT)
    # total_opening_Stock =                                   ##########
    Min_oreder_Qty = models.CharField(max_length=20)
    order_Id = models.CharField(max_length=20)
    customer_Name = models.ForeignKey(Client_Details, on_delete=models.PROTECT)
    order_Qty = models.CharField(max_length=20)
    planning_Qty = models.CharField(max_length=20)
    production_Start_Date = models.DateField()
    production_Close_Data = models.DateField()
    production_Status = models.CharField(max_length=20)
    planning_Qty2 = models.CharField(max_length=20)
    production_Qty = models.CharField(max_length=20)
    dispatch_Date = models.DateField()
    pcs = models.CharField(max_length=20)
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
    batch = models.CharField(max_length=20)
    pack_brand = models.CharField(max_length=20)
    unit = models.CharField(max_length=20)
    order_Qty2 = models.CharField(max_length=20)
    oc_remarks = models.CharField(max_length=20)
    b_Weight = models.CharField(max_length=20)
    shade = models.CharField(max_length=20)


class Prodution_Analysis(models.Model):
    create_Date = models.DateField()
    Design_analysis_id = models.CharField(max_length=20)
    seq_No = models.CharField(max_length=20)
    design_Name = models.CharField(max_length=20)
    Product = models.ForeignKey(Product, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    size = models.ForeignKey(Size, on_delete=models.PROTECT)
    category = models.ForeignKey(Cetegory, on_delete=models.PROTECT)
    finish = models.ForeignKey(Finish, on_delete=models.PROTECT)
    series = models.ForeignKey(Series, on_delete=models.PROTECT)
    # pre =                                                 #############
    # std =                                                   #############
    # com =                                                    #############
    # eco =                                                     #############
    total_Qty = models.CharField(max_length=20)
    base_Design_Name = models.CharField(max_length=20)
    weight = models.CharField(max_length=20)
    product_Pic_Upload = models.ImageField()
    desing_Type = models.CharField(max_length=20)
    desing_Status = models.CharField(max_length=20)
    machine = models.CharField(max_length=20)
    weight2 = models.CharField(max_length=20)
    concept_Name = models.CharField(max_length=20)
    concept = models.ForeignKey(Concept, on_delete=models.PROTECT)
    # total_opening_Stock =                                   ##########
    Min_oreder_Qty = models.CharField(max_length=20)
    order_Id = models.CharField(max_length=20)
    customer_Name = models.ForeignKey(Client_Details, on_delete=models.PROTECT)
    order_Qty = models.CharField(max_length=20)
    planning_Qty = models.CharField(max_length=20)
    production_Start_Date = models.DateField()
    production_Close_Data = models.DateField()
    production_Status = models.CharField(max_length=20)
    planning_Qty2 = models.CharField(max_length=20)
    production_Qty = models.CharField(max_length=20)
    dispatch_Date = models.DateField()
    pcs = models.CharField(max_length=20)
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
    batch = models.CharField(max_length=20)
    pack_brand = models.CharField(max_length=20)
    unit = models.CharField(max_length=20)
    order_Qty2 = models.CharField(max_length=20)
    oc_remarks = models.CharField(max_length=20)
    b_Weight = models.CharField(max_length=20)
    shade = models.CharField(max_length=20)


class Current_Stock(models.Model):
    date = models.DateField()
    ware_House_Name = models.CharField(max_length=20)
    loacation_1 = models.CharField(max_length=20)
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT)
    state = models.ForeignKey(State, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    pincode = models.ForeignKey(Pincode, on_delete=models.PROTECT)
    maximum_Stock = models.CharField(max_length=20)
    minimum_Stock = models.CharField(max_length=20)
    design_Name = models.CharField(max_length=20)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    size = models.ForeignKey(Size, on_delete=models.PROTECT)
    category = models.ForeignKey(Cetegory, on_delete=models.PROTECT)
    finish = models.ForeignKey(Finish, on_delete=models.PROTECT)
    series = models.ForeignKey(Series, on_delete=models.PROTECT)
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
    base_Design_Name = models.CharField(max_length=20)
    weight = models.CharField(max_length=20)
    product_Pic = models.ImageField()
    design_Type = models.CharField(max_length=20)
    design_Status = models.CharField(max_length=20)
    machine = models.CharField(max_length=20)
    weight =  models.CharField(max_length=20)
    max_Qty = models.CharField(max_length=20)
    min_Qty = models.CharField(max_length=20)
    finish = models.CharField(max_length=20)    
    concept_Name = models.CharField(max_length=20)
    concept = models.ForeignKey(Concept, on_delete=models.PROTECT)
    total_Opening_Stock = models.CharField(max_length=20)


class Stock_in(models.Model):
    date = models.DateField()
    ware_House_Name = models.CharField(max_length=20)
    location_1 = models.TextField()
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT)
    state = models.ForeignKey(State, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    pincode = models.ForeignKey(Pincode, on_delete=models.PROTECT)
    maximum_Stock = models.CharField(max_length=20)
    minimum_Stock = models.CharField(max_length=20)
    design_Name = models.CharField(max_length=20)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    size = models.ForeignKey(Size, on_delete=models.PROTECT)
    category = models.ForeignKey(Cetegory, on_delete=models.PROTECT)
    finish = models.ForeignKey(Finish, on_delete=models.PROTECT)
    series = models.ForeignKey(Series, on_delete=models.PROTECT)
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
    base_Design_Name = models.CharField(max_length=20)
    weight = models.CharField(max_length=20)
    product_Pic = models.ImageField()
    remarks = models.TextField()
    design_Type = models.CharField(max_length=20)
    design_Status = models.CharField(max_length=20)
    machine = models.CharField(max_length=20)
    weight =  models.CharField(max_length=20)
    max_Qty = models.CharField(max_length=20)
    min_Qty = models.CharField(max_length=20)
    finish = models.CharField(max_length=20)    
    concept_Name = models.CharField(max_length=20)
    concept = models.ForeignKey(Concept, on_delete=models.PROTECT)
    opening_Qty = models.CharField(max_length=20)
    recieve_Qty = models.CharField(max_length=20)
    total_Opening_Stock = models.CharField(max_length=20)           ##########

class Stock_Out(models.Model):
    date = models.DateField()
    po = models.CharField(max_length=20)
    invoice = models.CharField(max_length=20)
    order = models.CharField(max_length=20)
    design_Name = models.CharField(max_length=20)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    size = models.ForeignKey(Size, on_delete=models.PROTECT)
    category = models.ForeignKey(Cetegory, on_delete=models.PROTECT)
    finish = models.ForeignKey(Finish, on_delete=models.PROTECT)
    series = models.ForeignKey(Series, on_delete=models.PROTECT)
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
    base_Design_Name = models.CharField(max_length=20)
    weight = models.CharField(max_length=20)
    product_Pic = models.ImageField()
    remarks = models.TextField()
    design_Type = models.CharField(max_length=20)
    design_Status = models.CharField(max_length=20)
    machine = models.CharField(max_length=20)
    weight =  models.CharField(max_length=20)
    max_Qty = models.CharField(max_length=20)
    min_Qty = models.CharField(max_length=20)
    finish = models.CharField(max_length=20)    
    concept_Name = models.CharField(max_length=20)
    concept = models.ForeignKey(Concept, on_delete=models.PROTECT)
    opening_Qty = models.CharField(max_length=20)
    out_warding_Qty = models.CharField(max_length=20)
    Total_Opening_Stock = models.CharField(max_length=20)                   ########
    truck = models.CharField(max_length=20)
    remarks = models.TextField()
    ware_House_Name = models.CharField(max_length=20)
    location1 = models.TextField()
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT)
    state = models.ForeignKey(State, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    pincode = models.ForeignKey(Pincode, on_delete=models.PROTECT)

class Service_Module(models.Model):
    service_Call_Date =  models.DateField()
    service_Call_Number = models.CharField(max_length=20)
    service_Call_Time = models.TimeField()
    customer_Name = models.CharField(max_length=20)
    customer_Address = models.CharField(max_length=20)
    invioce_Number = models.CharField(max_length=20)
    po = models.CharField(max_length=20)
    invoice_Date = models.DateField()
    total_Qty = models.CharField(max_length=20)
    landmark = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    design_Name = models.CharField(max_length=20)
    size = models.CharField(max_length=10)
    brand = models.CharField(max_length=20)
    batch_Number = models.CharField(max_length=20)
    manufacturing_Date = models.DateField()
    shift = models.BooleanField("Day", default=True)
    design_Qty = models.CharField(max_length=20)
    factory_Service_Code = models.CharField(max_length=20)
    details_Of_Problem = models.CharField(max_length=20)
    designation = models.CharField(max_length=20)
    representative_Name = models.CharField(max_length=20)
    action_Date_taken = models.DateField()
    comments = models.TextField()

class Performa_Invoice(models.Model):
    Order_id = models.CharField(max_length=20)
    order_Date = models.DateField()
    Customer_Name = models.CharField(max_length=20)
    Billing_Address_line1 = models.TextField()
    zone = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    pincode = models.CharField(max_length=20)
    Contact_Name = models.CharField(max_length=20)
    contact_Phone = models.CharField(max_length=20)
    order_Type = models.CharField(max_length=20)
    order_status = models.CharField(max_length=20)
    order_Method = models.CharField(max_length=20)
    remarks = models.TextField()
    add_Order_line_Item = models.CharField(max_length=20)
    seq_No = models.CharField(max_length=20)
    Ware_House_Name = models.CharField(max_length=20)
    design_Name = models.CharField(max_length=20)
    product = models.CharField(max_length=20)
    brand = models.CharField(max_length=20)
    size = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    finish = models.CharField(max_length=20)
    series = models.CharField(max_length=20)
    grade = models.CharField(max_length=20)
    base_Design_Name = models.CharField(max_length=20)
    weight = models.CharField(max_length=20)
    product_Pic = models.ImageField()
    remarks = models.TextField()
    design_Type = models.CharField(max_length=20)
    design_Status = models.CharField(max_length=20)
    machine = models.CharField(max_length=20)
    weight =  models.CharField(max_length=20)
    max_Qty = models.CharField(max_length=20)
    min_Qty = models.CharField(max_length=20)
    finish = models.CharField(max_length=20)    
    concept_Name = models.CharField(max_length=20)
    concept = models.CharField(max_length=20)
    total_opening_Stock = models.CharField(max_length=20)         ########
    min_order_Qty = models.CharField(max_length=20)
    pcs = models.CharField(max_length=20)
    grade = models.CharField(max_length=20)
    batch = models.CharField(max_length=20)
    pack_brand = models.CharField(max_length=20)
    unit = models.CharField(max_length=20)
    order_Qty = models.IntegerField()
    oc_Remark = models.CharField(max_length=20)
    b_weight = models.IntegerField()
    shade = models.CharField(max_length=20)
    shipping_Address = models.TextField()
    location_1 = models.TextField()
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    pin_Code = models.CharField(max_length=20)
    total_Weight =  models.IntegerField()                                  
    # current_Stock =                                   #########
    
    def save(self):
        self.total_Weight = self.b_weight * self.order_Qty
        return super(Performa_Invoice, self).save() 

class Planning_For_Classified(models.Model):
    planning_ID = models.CharField(max_length=20)
    Planning_Start_Date = models.DateField()
    planning_End_Date = models.DateField()
    customer_Name = models.CharField(max_length=20)
    Billing_Address_Line1 = models.CharField(max_length=20)
    zone = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    pincode = models.CharField(max_length=20)
    contact_Name = models.CharField(max_length=20)
    contact_Phone = models.CharField(max_length=20)
    order_Type = models.CharField(max_length=20)
    order_Status = models.CharField(max_length=20)
    order_mathod = models.CharField(max_length=20)
    remarks = models.TextField()
    add_Order_Line_item = models.CharField(max_length=20)
    seq_No = models.CharField(max_length=20)
    # total_Open_Quantity =                            #########
    design_Name = models.CharField(max_length=20)
    product = models.CharField(max_length=20)
    brand = models.CharField(max_length=20)
    size = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    finish = models.CharField(max_length=20)
    series = models.CharField(max_length=20)
    grade = models.CharField(max_length=20)
    base_design_naem = models.CharField(max_length=20)
    weight = models.CharField(max_length=20)



