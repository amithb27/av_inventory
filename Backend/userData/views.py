from django.shortcuts import  get_object_or_404
from django.urls import reverse
from django.shortcuts import render
from django.template.loader import render_to_string
from .ProjectUtilities import CustomsendMail
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password
import requests
from django.contrib.auth import authenticate, login,logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view 
from rest_framework.views import APIView
from rest_framework import status 
from .models import *
from django.contrib.contenttypes.models import ContentType
from .serializers import *
from django.contrib.auth.decorators import permission_required
from django.utils import timezone
from django.contrib.auth.models import Permission 

#**-----------------------------------------------------------------------**

#utility  API'S

@login_required 
@api_view(["POST"])
def send_mail_with_login_creds(request,pk):
    """
    Sends an email with login credentials to an employee.

    This view function receives a POST request with the email and password data. 
    And sends an Email with login credentials

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the employee.

    Returns:
        - If the email is sent successfully:
            - JSON response with a success message: {"message": "Email sent"}
            - Status code: 200 (OK)
        - If there is an error sending the email:
            - JSON response with an error message: {"message": <error_message>}
            - Status code: 400 (Bad Request)
    """
    data = request.data
    my_date = timezone.now()
    emp= get_object_or_404(Employee,pk=pk)
    try :
        emp =  Employee.objects.get(pk=pk)
    except Exception as e :
        return Response({"message" : "Employee Not exist "},status= status.HTTP_404_NOT_FOUND)
    year = my_date.strftime("%Y")
    logincredsContext={
        "name" :emp.name,
        "email"   :data["email"],
        "password":data["password"],
        "joiningDate" : emp.joining_Date,
        "year" : year
    }
    template = render_to_string(template_name="logincreds.html" ,context=logincredsContext)
    
    sent =  CustomsendMail(template=template , subject= "Login Details ",
                           to_Person=emp.email , message="Login Details"
                           )
    
    if sent == True :
        return Response(data = {"Message":"employee created And sent Login creds succesfully"} , status=status.HTTP_200_OK )
    else:
        return Response(data={
            sent
        }, status=status.HTTP_400_BAD_REQUEST)


def Template(request):
    my_date = timezone.now()
    joiningDate = my_date.strftime("%d - %B - %Y")
    year = my_date.strftime("%Y")
    birthDayContext = {
        "name" :"Employee",
        "year" : year
    }
    aniversaryContext = {
        "name" :"Employee",
        "year" : year,
        "workingYears" : 2
    }
    logincredsContext = {
        "name" :"Employee",
        "email"   :"Employee@gmail.com",
        "password":"*******",
        "joiningDate" : joiningDate
    }
    
    return render(request = request , template_name = "forgetpassword.html", context = birthDayContext)


@api_view(["POST"])
def login_user(request):
       
    # Logs in a user with the provided credentials.

    # Args:
    #     request (HttpRequest): The HTTP request object.

    # Returns:
    #     - If the authentication is successful:
    #         - Empty response
    #         - Status code: 200 (OK)
    #     - If the authentication fails:
    #         - JSON response with an error message: "cannot login with the provided credentials"
    #         - Status code: 401 (Unauthorized)
    requestedUser = request.data["username"]
    password = request.data["password"]
    user = authenticate(request, username = requestedUser , password = password)   
    if user is not None :
        login(request, user)
        return Response(data="sucessfully loggedIn", status=status.HTTP_200_OK)
    return Response(data="cannot login with the provided credentials " ,status=status.HTTP_401_UNAUTHORIZED)

@login_required 
@api_view(["GET"])
def logout_user(request):
    
    # Logs out the currently authenticated user.

    # Args:
    #     request (HttpRequest): The HTTP request object.

    # Returns:
    #     - JSON response with a success message: "logout success"
    #     - Status code: 200 (OK)
    logout(request)
    return Response(data={
        "message":"logout success"}, status=status.HTTP_200_OK)


@login_required 
@api_view(["POST"])  
def send_mail_with_media(request): 
    # This view requires the user to be authenticated
    
    # Retrieve the data from the request
    data = request.data
    
    # Get the image file from the request
    file = request.FILES["image"]
    
    # Extract the file name and content
    file_name = file.name
    content = file.read()
    
    # Prepare the parameters for sending the email
    email_subject = data["subject"]
    email_message = data["message"]
    to_person = data["to_Person"]
    
    # Render the email template with in-line media (image attachment)
    template = render_to_string(template_name="birthday.html", imageFiles=[(file_name, content)])
    
    # Send the email using the CustomsendMail function
    result = CustomsendMail(subject=email_subject, message=email_message, to_Person=to_person, template=template)
    
    if result == True:
        # If the email was sent successfully, return a success response
        return Response({"message": "Mail sent successfully"}, status=status.HTTP_200_OK)
    else:
        # If there was an error sending the email, return an error response with the result
        return Response(data=result, status=status.HTTP_400_BAD_REQUEST)


#**-----------------------------------------------------------------------**

#user API's
 
def delete_user(self, request,pk):

    try :
        admin =  user.objects.get(pk=pk)
    except Exception as e :
        return Response({"message" : "Admin Not exist "},status= status.HTTP_404_NOT_FOUND)
    admin.is_active = False

@login_required
@api_view(["POST"]) 
def post_user(self,request):
    
    # Handles the POST request to create a new user.
    
    # Args:
    #     request (HttpRequest): The HTTP request object.

    # Returns:
    #     - JSON response from the email service API
    #     - Status code: 200 (OK)
    #     - JSON response with validation errors
    #     - Status code: 400 (Bad Request)
    
    serializer = UserSerializer(data=request.data , 
                                context = {"employee":request.data["employee"]})
    if serializer.is_valid():
        data_Object = serializer.save()
        print(int(data_Object["pk"]))
        response= requests.post(url=request.build_absolute_uri(reverse(viewname= "email_Service" , kwargs=({"pk": int(data_Object["pk"])}) )), data=data_Object)
        return Response(data=response.json() ,status=response.status_code)
    else:    
        return Response( serializer.errors , status= status.HTTP_400_BAD_REQUEST)
    

def update_user(self ,request ):
    # Handles the PATCH request to update the user password.
    
    # Args:
    #     request (HttpRequest): The HTTP request object.

    # Returns:
    #     - JSON response with a success message: "Password changed"
    #     - Status code: 200 (OK)
    #     - JSON response with validation errors
    #     - Status code: 400 (Bad Request)
    
    requested_User = request.user
    serializer =  UserSerializer(data=request.data , instance=requested_User ) 
    if serializer.is_valid():
        serializer.save()
        return Response(data={"message":"Password changed "} ,status=status.HTTP_200_OK)
    return Response(data=serializer.errors , status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def forgot_user_password(request):
    # Retrieve the data from the request
    data = request.data
    mail = data["email"]
    
    # Get the requested user based on the provided email
    requested_user = get_object_or_404(user, email=mail)
    
    # Generate a new password
    password = makePassword()
    
    # Set the new password for the requested user
    requested_user.set_password(password)
    requested_user.save()
    
    # Get the current year
    my_date = timezone.now()
    year = my_date.strftime("%Y")
    
    # Prepare the context for the password reset email template
    logincredsContext = {
        "password": password,
        "year": year
    }
    
    # Render the password reset email template
    template = render_to_string(template_name="forgetpassword.html", context=logincredsContext)
    
    # Send the password reset email
    CustomsendMail(message="New password", subject="New password", template=template)
    
    return Response(
        data={"message": "Check your registered email for a new password"},
        status=status.HTTP_200_OK
    )


@permission_required("userData.change_user")
@login_required 
@api_view(['POST'])
def change_user_password(request):
    # Retrieve the data from the request
    data = request.data
    
    # Get the requested user based on the authenticated user making the request
    requested_user = request.user
    
    # Extract the current and new passwords from the data
    curr = data["curr"]
    new = data["new"]
    
    # Get the current password of the requested user
    old_password = requested_user.password
    
    # Check if the current password provided matches the user's current password
    check = check_password(old_password, curr)
    
    if check:
        # If the current password is correct, set the new password for the user
        requested_user.set_password(new)
        requested_user.save()
        
        return Response(data={"message": "Password changed successfully"}, status=status.HTTP_200_OK)
    
    # If the current password is incorrect, return an error response
    return Response(data={"message": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)


#**-----------------------------------------------------------------------**

# admin API's
@login_required
@api_view(["POST"]) 
def post_admin(self,request): 
                           
        # Handles the POST request to create a new admin user.


        # Args:
        #     request (HttpRequest): The HTTP request object.

        # Returns:
        #     - JSON response with a success message: "Created Admin"
        #     - Status code: 201 (Created)
        #     - JSON response with validation errors
        #     - Status code: 400 (Bad Request)
        #     - JSON response with an error message: "Admin Limit exceeded"
        #     - Status code: 403 (Forbidden)
        
            serializer = AdminSerializer(data=request.data )
            if serializer.is_valid():
                admin = request.user
                if  admin.join_Count == 0 :
                    return Response(data={"message":"Admin Limit exceeded"}
                                    , status=status.HTTP_403_FORBIDDEN
                    )
                serializer.save()
                admin.join_Count -=1
                admin.save()
                return Response(data={
                                    "message":"Created Admin"}, 
                                status= status.HTTP_201_CREATED
                )
            return Response( serializer.errors , status= status.HTTP_400_BAD_REQUEST)
        

def delete_admin(self, request,pk):
    try :
        admin =  user.objects.get(pk=pk)
    except Exception as e :
        return Response({"message" : "user Not exist "},status= status.HTTP_404_NOT_FOUND)
    admin.is_active = False


#**-----------------------------------------------------------------------**

# Role apis
@login_required
@api_view(["GET"]) 
def get_all_roles(self,request): 
    # Handles the GET request to retrieve all Roles.

    # Args:
    #     request (HttpRequest): The HTTP request object.
    #     role (str, optional): The name of the role to retrieve its ancestors. Defaults to None.

    # Returns:
    #     - JSON response with serialized data of the available roles or ancestors
    #     - Status code: 200 (OK)
    
    available_roles = RoleHierarchy.objects.all()
    print(available_roles)
    serializedData = RoleHierarchySerializer(available_roles , many=True)
    return Response(serializedData.data)
    
@api_view(["GET"])
@login_required
@permission_required(["userData.view_role"])
def get_role(request,pk):
    try :
        role =  Role.objects.get(pk=pk)
    except Exception as e :
        return Response({"message" : "Role not exists "},status= status.HTTP_404_NOT_FOUND)
    serializers =RoleSerializer(role )
    return Response(data=serializers.data, status=status.HTTP_200_OK)   
  
  
@api_view(["GET"])       
@login_required
@permission_required("userData.view_rolehierarchy")
def get_all_senior_roles(request,role):
    try :
        role_object =  RoleHierarchy.objects.get(role=role)
    except Exception as e :
        return Response({"message" : "notification Not exist "},status= status.HTTP_404_NOT_FOUND) 
    available_reporting_roles = role_object.get_ancestors()
    serializer = RoleHierarchySerializer(available_reporting_roles , many = True )
    return  Response(data= serializer.data , status= status.HTTP_200_OK)
   
@login_required
@api_view(["POST"])   
def post_role(self , request):
    data = request.data
    serializer=  RoleSerializer(data={"name":(data["name"]).upper()})
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"created Role"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors , status= status.HTTP_400_BAD_REQUEST)


def update_role(self,request,pk):
        try :
            instance =  Role.objects.get(pk=pk)
        except Exception as e :
            return Response({"message" : "Role Not exist "},status= status.HTTP_404_NOT_FOUND)
        serializer = RoleSerializer(data=request.data , instance= instance)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"updated succsusful"} , status=status.HTTP_200_OK)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
   
   
def delete_role(self, request,pk):
    role = get_object_or_404(Role , pk=pk)
    role.is_active = False 
    role.save()
   

#**-----------------------------------------------------------------------**    

#Role hierarchy API's

@login_required
@api_view(["GET"]) 
def get_all_hierarchy_tree(request):
    hierarchy = RoleHierarchy.objects.all()
    serializer = RoleHierarchySerializer(hierarchy , many =True)
    return Response(data=serializer.data , status=status.HTTP_200_OK)


def update_role_hierarchy(request , pk ):
    data = request.data
    try :
        instance =  RoleHierarchy.objects.get(pk=pk)
    except Exception as e :
        return Response({"message" : "Employee Not exist "},status= status.HTTP_404_NOT_FOUND)
    
    serializer = RoleHierarchySerializer(data=data , instance=instance )
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.errors , status= status.HTTP_400_BAD_REQUEST)


def delete_role_hierarchy(request , role):
        """
        Handles the DELETE request to update a role.
        
        Args:
            request (HttpRequest): The HTTP request object.
            role (str): The role name to delete.

        Returns:
            - JSON response with the delete of role
            - Status code: 200 (OK)
            - JSON response with conflits while deleting 
            - Status code: 400 (Bad Request)
        """
        cur_Role = RoleHierarchy.objects.get(role= role)
        child  = cur_Role.get_children_count()
        if child == 0 :
            cur_Role.is_active = False
            return Response({"message":"Role Deleted"} , status=status.HTTP_200_OK)
        else:
            return Response({"message ":"Delete the sub roles first"} , status=status.HTTP_400_BAD_REQUEST)

@login_required
@api_view(["POST"]) 
def post_rolehierarchy(request):

    # Handles the POST request to create a new role.

    # Args:
    #     request (HttpRequest): The HTTP request object.

    # Returns:
    #     - JSON response with a success message: "created"
    #     - Status code: 201 (Created)
    #     - JSON response with validation errors
    #     - Status code: 400 (Bad Request)

    requestedUser = request.user
    if requestedUser.join_Count > 0 :
        roleData=request.data  
        role = roleData["role"]
        reporting_role = roleData["reporting_role"]
        try :
            is_unique = RoleHierarchy.objects.get(role = role)
            return( Response({"message":"Role Already Exists"} , 
                                status=status.HTTP_400_BAD_REQUEST)
                    )
        except Exception as e:
            if reporting_role == "self":
                root = RoleHierarchy.add_root(role = role , reporting_role = "self")
                requestedUser.join_Count -= 1 
            else:
                try :
                    parent = RoleHierarchy.objects.get(role = reporting_role)
                    parent.add_child(role = role , reporting_role = reporting_role)
                    requestedUser.join_Count -= 1 
                except ObjectDoesNotExist as e :         
                    return Response(data = {"message" : "create reporting role First " },status= status.HTTP_400_BAD_REQUEST)
            return Response({"message":"role Created" }, status=status.HTTP_200_OK)
    return( Response({"message":"Admin Limit exceeds"} , status=status.HTTP_401_UNAUTHORIZED))
    

#**-----------------------------------------------------------------------** 

#Employee API's

@login_required
@api_view(["GET"]) 
@permission_required("userData.view_employee") 
def get_all_employees(request):
    data = Employee.objects.all()
    serializer = EmployeeSerializer(data, many=True)   
    return Response(serializer.data, status=status.HTTP_200_OK)
 
 
@login_required
@api_view(['GET'])
@permission_required("userData.view_employee")  
def get_employee(request,pk):
    
    # Handles the GET request to retrieve allEmployess.
    # Args:
    #     request (HttpRequest): The HTTP request object.

    # Returns:
    #     - JSON response with serialized data of the available Employess
    #     - Status code: 200 (OK)
    try :
        emp =  Employee.objects.get(pk=pk)
    except Exception as e :
        return Response({"message" : "Employee Not exist "},status= status.HTTP_404_NOT_FOUND)      
    data=EmployeeSerializer(emp)
    return Response(data.data , status=status.HTTP_302_FOUND)


@login_required
@api_view(["GET"]) 
def get_employees_with_role(request , role):
    emp = Employee.objects.filter(role=role)
    serilizer = EmployeeSerializer(emp , many = True)
    return Response(serilizer.data , status=status.HTTP_200_OK)


@login_required
@api_view(["POST","GET"])
@permission_required(["userData.view_employee"])        
def get_employeeId_for_native_users(request):
    """
    Retrieves the mobile profile for an authenticated user.

    This view function checks if the user is accessing the profile from a mobile device based on the user agent.
    And sends Back the employee Id

    Returns:
        - If the user is on a mobile device and not an admin:
            - JSON response with the employee ID: {"id": employee_id}
            - Status code: 200 (OK)
        - If the user is an admin:
            - JSON response with a "permission denied" message: {"message": "permission is an admin"}
            - Status code: 404 (Not Found)
        - If the user is not on a mobile device:
            - Empty JSON response
            - Status code: 204 (No Content)
    """
    
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    devices = ['mobile','android','iphone','tablet','ipad']
    is_Mobile_User = False
    for device  in devices:
        if device in user_agent:
            is_Mobile_User = True
    if is_Mobile_User :
        user = request.user
        if user.is_Admin == False :
            emp = user.employee
            return Response(data={"id":emp.employee_Id} , status=status.HTTP_200_OK)
        else :
            return Response(data={"message" : " requested user is Not an employee "} , status=status.HTTP_404_NOT_FOUND)
    return Response(data={"message":"Not a mobile device"} , status=status.HTTP_204_NO_CONTENT)


@login_required
@api_view(['GET'])
@permission_required("userData.add_employee")
def post_employee(request):
        # Get the user making the request
        requestedUser = request.user
       
        # Handle POST request to create a new employee
        
        # Create a serializer instance with the request data
        serializer = EmployeeSerializer(data=request.data, context={"requestedUser": requestedUser, "role": request.data["role"]})
        
        if serializer.is_valid():
            # Save the employee and get the primary key (pk) and email
            (pk, email) = serializer.save()
            
            # Check if the employee is also a web user
            is_Web_user = request.data["web_User"]
         
            
            if is_Web_user:
                # If the employee is also a web user, send a request to create a user
                
                # Construct the URL for the create_user view
                create_user_url = request.build_absolute_uri(reverse(viewname="create_user"))
                
                # Prepare the data for the create user request
                user_data = {
                    "email": email,
                    "employee": pk
                }
                
                # Send a POST request to create the user
                response = requests.post(url=create_user_url, data=user_data)
                
                return Response(data=response.json(), status=response.status_code)
            
            # Return a success response indicating that the employee was created
            return Response(data={"Message": "Employee created"}, status=status.HTTP_200_OK)
        
        # Return an error response with serializer errors if the data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['PUT'])
@permission_required("userData.change_employee")   
def update_employee(request,pk):
    try :
        emp =  Employee.objects.get(pk=pk)
    except Exception as e :
        return Response({"message" : "Employee Not exist "},status= status.HTTP_404_NOT_FOUND)
    """
    Handles the PUT request to update a employee.
    
    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the employee to update.

    Returns:
        - Status code: 200 (OK)
        - JSON response with validation errors
        - Status code: 400 (Bad Request)
    """
    serializer = EmployeeSerializer(emp, data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
           
@login_required
@api_view(['DELETE'])
@permission_required("userData.change_employee")    
def delete_employee(request,pk):  
    """
        Handles the DELETE request to Remove a employee.
        
        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The primary key of the employee to update.

        Returns:
            - Status code: 200 (OK)
            - JSON response with validation errors
            - Status code: 400 (Bad Request)
    """
    try :
        emp =  Employee.objects.get(pk=pk)
    except Exception as e :
        return Response({"message" : "Employee Not exist "},status= status.HTTP_404_NOT_FOUND) 
    emp.is_Active = False
    return Response(status=status.HTTP_204_NO_CONTENT)   


#**-----------------------------------------------------------------------** 

# Product API's

@login_required
@api_view(["GET"]) 
def get_all_products(request):
    Products = Product.objects.all()
    serializer = ProductSerializer(Products, many=True)
    # return JsonResponse({"drinks": serializers.data})
    return Response(serializer.data)
     
  
@login_required
@api_view(["POST"]) 
def post_product(request):  
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)   
  

#**-----------------------------------------------------------------------** 

# Brands API's

@login_required
@api_view(["GET"]) 
def get_all_brands(request):
        drinks = Brand.objects.all()
        serializer = BrandSerialilzer(drinks, many=True)
        # return JsonResponse({"drinks": serializers.data})
        return Response(serializer.data)
        

@login_required    
@api_view(['POST'])
def post_brand(request):
    serializer = BrandSerialilzer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


#**-----------------------------------------------------------------------** 

#Units API's

@login_required
@api_view(["GET"]) 
def get_all_units(request):
    drinks = Unit.objects.all()
    serializer = UnitSerializer(drinks, many=True)
    # return JsonResponse({"drinks": serializers.data})
    return Response(serializer.data)


@login_required
@api_view(["POST"]) 
def post_unit(request) :
    serializer = UnitSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)      


#**-----------------------------------------------------------------------**
 
#Units API's
@login_required
@api_view(["GET"]) 
def get_all_sizes(request):
    drinks = Size.objects.all()
    serializer = SizeSeriallizer(drinks, many=True)
    # return JsonResponse({"drinks": serializers.data})
    return Response(serializer.data)


@login_required
@api_view(["POST"]) 
def post_size(request):
    serializer = SizeSeriallizer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
  

#**-----------------------------------------------------------------------**

#Category API's

@login_required
@api_view(["GET"]) 
def get_all_categories(request):
    drinks = Cetegory.objects.all()
    serializer = CetegorySerializer(drinks, many=True)
    # return JsonResponse({"drinks": serializers.data})
    return Response(serializer.data) 
   
      
@login_required
@api_view(["POST"]) 
def post_category(request):
    serializer = CetegorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


#**-----------------------------------------------------------------------**

#notifications API's

@permission_required("userData.change_notification")
@login_required
@api_view(['UPDATE'])
def update_notifications_with_user(request):
    try:
        # Get the notification based on the provided primary key (pk)
        notification = Notification.objects.get(pk=pk)
    except Exception as e:
        # If the notification does not exist, return an error response
        return Response({"message": "Notification does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    # Mark the notification as inactive
    notification.is_active = False
    notification.save()
    
    # Return a success response indicating the notification was updated
    return Response(status=status.HTTP_200_OK)


@login_required
@api_view(["GET"]) 
def get_notifications_with_user(request):
    # Get the requested user based on the authenticated user making the request
    requested_user = request.user
    
    # Retrieve all notifications for the requested user
    notifications = requested_user.notifications.all()
    
    # Serialize the notifications
    serializer = NotificationSerializer(notifications, many=True)
    
    if serializer.is_valid():
        # Return the serialized data in the response
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    
#**-----------------------------------------------------------------------**    

#Permissions API's
@login_required
@api_view(["GET"]) 
def get_user_permissions(request):
    appContent = ContentType.objects.get(app_name = "userData")
    perms = Permission.objects.filter(contenttype = appContent)
    
@login_required
@api_view(["POST"])     
def post_permission(request,pk):
    data = request.data

    try :
        employee =  Employee.objects.get(pk=pk)
    except Exception as e :
        return Response({"message" : "Employee Not exist "},status= status.HTTP_404_NOT_FOUND)
    user = employee.user 
    user.user_permissions.add()

