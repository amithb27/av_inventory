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
# Create your views here.

class Employee_Permission(APIView):

    @method_decorator(login_required)
    @method_decorator(permission_required("userData.view_user"))
    def get(request):
        appContent = ContentType.objects.get(app_name = "userData")
        perms = Permission.objects.filter(contenttype = appContent)
   
    @method_decorator(login_required)
    @method_decorator(permission_required("userData.change_user"))
    def post(request,pk):
        data = request.data
 
        try :
            employee =  Employee.objects.get(pk=pk)
        except Exception as e :
            return Response({"message" : "Employee Not exist "},status= status.HTTP_404_NOT_FOUND)
        user = employee.user 
        user.user_permissions.add()

@login_required()
@api_view(["POST","GET"])
@permission_required(["userData.view_employee"])        
def MobileProfile(request):
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


@api_view(["POST"])
def SendMail(request,pk):
    print(request.data)
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

# this view is for just to see the templates ...
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
def Login(request):
       
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


@api_view(["GET"])
def Logout(request):
    
    # Logs out the currently authenticated user.

    # Args:
    #     request (HttpRequest): The HTTP request object.

    # Returns:
    #     - JSON response with a success message: "logout success"
    #     - Status code: 200 (OK)
    logout(request)
    return Response(data={
        "message":"logout success"}, status=status.HTTP_200_OK)

#Updating password 2 Views for  admin
class Create_Admin(APIView):        
    #  API view to create a new admin user.
    
        # @method_decorator(login_required)
        # @permission_required("userData.add_user")
        def post(self,request): 
                           
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
        
        @method_decorator(login_required)
        @method_decorator(permission_required("userData.change_user"))
        def delete(self, request,pk):
            try :
                admin =  user.objects.get(pk=pk)
            except Exception as e :
                return Response({"message" : "user Not exist "},status= status.HTTP_404_NOT_FOUND)
            admin.is_active = False
#Updating password 2 Views for user
class Create_User(APIView ):
    
    #    API view to create a new user and update user password.
    
        # @method_decorator(login_required)
        # @method_decorator(permission_required("userData.add_user"))
        def post(self,request):
           
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
    
      
        @method_decorator(login_required)
        def patch(self ,request ):
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
        
        @method_decorator(login_required)
        @method_decorator(permission_required("userData.change_user"))
        def delete(self, request,pk):

            try :
                admin =  user.objects.get(pk=pk)
            except Exception as e :
                return Response({"message" : "Admin Not exist "},status= status.HTTP_404_NOT_FOUND)
            admin.is_active = False
#can change role name      
class Role_View(APIView):
    #    API view to create, retrieve, update roles.
    @method_decorator(login_required)
    @method_decorator(permission_required(["userData.add_role"])) 
    def post(self , request):
        data = request.data
        serializer=  RoleSerializer(data={"name":(data["name"]).upper()})
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"created Role"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status= status.HTTP_400_BAD_REQUEST)

    
    @method_decorator(login_required)
    @method_decorator(permission_required(["userData.view_role"]))   
    def get(self,request):
        roles = Role.objects.all()
        serializers = RoleSerializer(roles , many = True)
        return Response(data=serializers.data , status=status.HTTP_200_OK)    
    
    @method_decorator(login_required)
    @method_decorator(permission_required(["userData.view_role"]))
    def patch(self,request,pk):
        try :
            instance =  Role.objects.get(pk=pk)
        except Exception as e :
            return Response({"message" : "Role Not exist "},status= status.HTTP_404_NOT_FOUND)
        serializer = RoleSerializer(data=request.data , instance= instance)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"updated succsusful"} , status=status.HTTP_200_OK)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
      
    @method_decorator(login_required)
    @method_decorator(permission_required("userData.change_role"))
    def delete(self, request,pk):
        admin = get_object_or_404(Role , pk=pk)
        admin.is_active = False  
              
@api_view(["GET"])
@login_required
@permission_required(["userData.view_role"])
def Get_Role(request,pk):
    roles = get_object_or_404(Role,pk=pk  )
    try :
        emp =  Employee.objects.get(pk=pk)
    except Exception as e :
        return Response({"message" : "Employee Not exist "},status= status.HTTP_404_NOT_FOUND)
    serializers =RoleSerializer(roles )
    return Response(data=serializers.data, status=status.HTTP_200_OK)   
class RoleHierarchy_View(APIView):
    #    API view to create, retrieve, update roles.
     
    @method_decorator(permission_required("userData.add_rolehierarchy"))
    @method_decorator(login_required)  
    def post(self,request):
        
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
   
    @method_decorator(permission_required("userData.change_rolehierarchy"))
    @method_decorator(login_required) 
    def patch(self ,request , pk ):
        data = request.data
        try :
            instance =  RoleHierarchy.objects.get(pk=pk)
        except Exception as e :
            return Response({"message" : "Employee Not exist "},status= status.HTTP_404_NOT_FOUND)
        
        serializer = RoleHierarchySerializer(data=data , instance=instance )
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.errors , status= status.HTTP_400_BAD_REQUEST)
    
    
    @method_decorator(login_required)
    @method_decorator(permission_required("userData.view_rolehierarchy"))
    def get(self,request): 
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
    
    
    @method_decorator(login_required)
    @method_decorator(permission_required("userData.change_rolehierarchy") )
    def delete(request , role):
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


@api_view(["GET"])       
@login_required
@permission_required("userData.view_rolehierarchy")
def GetRoleNode(request,role):
    
    # Handles the GET request to retrieve a specific Role with role name.

    # Args:
    #     request (HttpRequest): The HTTP request object.
    #     role (str, optional): The name of the role to retrieve its ancestors. Defaults to None.

    # Returns:
    #     - JSON response with serialized data of the available roles or ancestors
    #     - Status code: 200 (OK)

    try :
        role_object =  RoleHierarchy.objects.get(role=role)
    except Exception as e :
        return Response({"message" : "notification Not exist "},status= status.HTTP_404_NOT_FOUND) 
    
    available_reporting_roles = role_object.get_ancestors()

    serializer = RoleHierarchySerializer(available_reporting_roles , many = True )
    return  Response(data= serializer.data , status= status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@login_required
@permission_required("userData.change_employee")
def Employees_List(request):

    requestedUser = request.user
    
    if request.method == 'GET':
        data = Employee.objects.all()
        serializer = EmployeeSerializer(data, many=True)
        return Response(serializer.data ,status=status.HTTP_200_OK)
    
    
    elif request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data ,context = {"requestedUser" : requestedUser ,                                                                  "role":request.data["role"]})
        if serializer.is_valid():
            (pk,email) = serializer.save()
            is_Web_user = request.data["web_User"]
            print(is_Web_user,"asdfdsf")
            if is_Web_user :
                response =  requests.post(url=request.build_absolute_uri(reverse(viewname= "create_user"  )) , data={
                    "email" :email,
                    "employee" : pk
                    })
                return Response(data=response.json(),status=response.status_code)
            return Response(data = {"Message":"employee created"} ,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
@api_view(['PUT', 'DELETE','GET'])
@permission_required("userData.change_employee")
def Employees_Details(request, pk):
    id = request.session
    print(id)
    #API view to retrieve, update, or delete an employee.
    # Args:
    #     request (HttpRequest): The HTTP request object.
    #     pk (int): The employee ID.

    # Returns:
    #     Response: The HTTP response containing the serialized employee data or a success/error message.

    try :
        emp =  Employee.objects.get(pk=pk)
    except Exception as e :
        return Response({"message" : "Employee Not exist "},status= status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        
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
    
    elif request.method == 'DELETE':
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
        emp.is_Active = False
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'GET':
        
        # Handles the GET request to retrieve allEmployess.

        # Args:
        #     request (HttpRequest): The HTTP request object.

        # Returns:
        #     - JSON response with serialized data of the available Employess
        #     - Status code: 200 (OK)
        
        data=EmployeeSerializer(emp)
        return Response(data.data , status=status.HTTP_302_FOUND)
    
@login_required 
@api_view(["POST"])  
def TriggerMail(request): 
    #it will email sender function with attachment files or 
    #To render in-line media in the template
    data = request.data
    file = request.Files["image"]
    file_name = file.name
    content = file.read()
    result =CustomsendMail(subject= data["subject"] , message=data["message"],
                   to_Person=data["to_Person"] ,
                   template=render_to_string(template_name="birthday.html" ,
                   imageFiles = [(file_name , content)],    
    ))
    if result==True :
        return Response({"message":"mail sent successfully"} , status= status.HTTP_200_OK)
    else:
        return Response(data=result , status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def ForgotPassword(request):
    data = request.data
    mail = data["email"]
    requested_user = get_object_or_404(user , email = mail)
    password = makePassword()
    requested_user.set_password(password)
    requested_user.save()
    my_date = timezone.now()
    year = my_date.strftime("%Y")
    logincredsContext={
        "password":password,
        "year" : year
    }
    template = render_to_string(template_name="forgetpassword.html" ,context=logincredsContext)
    CustomsendMail(message="New password" , subject="New password",
                   template=template, )
    return Response(
        data={"message":"Check your registered email for new Password "}
        ,status=status.HTTP_200_OK
    )
  
@api_view(['POST'])
@login_required
def ResetPassword(request):
    data = request.data
    requested_user = request.user
    curr = data["curr"]
    new = data["new"]
    old_password = requested_user.password
    check = check_password(old_password , curr)
    if check:
        requested_user.set_password(new)
        requested_user.save()
        return Response(data={"message":
            "password Changed suscessfully"}
            ,status=status.HTTP_200_OK
        )
    return Response(data={"message":"Old password is incorrect"} ,
                    status=status.HTTP_400_BAD_REQUEST
    )

class NotificationManager(APIView):

    @method_decorator(login_required)
    def get(request):
        requested_user = request.user
        notifications =  requested_user.notifications.all()
        seriliazer = NotificationSerializer(notifications , many= True)
        if seriliazer.is_valid():
            return Response({"data":seriliazer.data}, status= status.HTTP_200_OK)
    
    @method_decorator(login_required)
    def update(request , pk ):
        try :
            notification =  Notification.objects.get(pk=pk)
        except Exception as e :
            return Response({"message" : "notification Not exist "},status= status.HTTP_404_NOT_FOUND)
        notification.is_active = False
        notification.save()
        
        
        