from django.shortcuts import  get_object_or_404
from django.urls import reverse
from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import render_to_string
from smtplib import SMTPException
import requests
from django.conf import settings
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
        employee = get_object_or_404(Employee,pk)
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
    
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    devices = ['Mobile','Android','iPhone','Tablet','iPad']
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
    
    year = my_date.strftime("%Y")
    logincredsContext={
        "name" :emp.name,
        "email"   :data["email"],
        "password":data["password"],
        "joiningDate" : emp.joining_Date,
        "year" : year
    }
    print(emp.email)
    template = render_to_string(template_name="logincreds.html" ,context=logincredsContext)
    
    try  :
        send_mail(
    html_message=template,
    subject ="Email_testing",
    message= "...Analytics Valley...",
    from_email=settings.EMAIL_HOST_USER,
    recipient_list=[emp.email,],
    fail_silently=False,
    
        ) 
        return Response(data = {"Message":"employee created And sent Login creds succesfully"} , status=status.HTTP_200_OK )
    except  SMTPException  as e:
        return Response(data={
            "message":e 
        }, status=status.HTTP_400_BAD_REQUEST)


# this view is for just to see the templates ...
def Template(request):
    my_date = timezone.now()
    joiningDate = my_date.strftime("%d - %B - %Y")
    year = my_date.strftime("%Y")
    birthDayContext={
        "name" :"Employee",
        "year" : year
    }
    aniversaryContext={
        "name" :"Employee",
        "year" : year,
        "workingYears" : 2
    }
    logincredsContext={
        "name" :"Employee",
        "email"   :"Employee@gmail.com",
        "password":"*******",
        "joiningDate" : joiningDate
    }
    
    return render(request=request , template_name="birthday.html", context=birthDayContext)

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
        return Response(data="sucessfully loggedIn" ,status=status.HTTP_200_OK)
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

class Create_Admin(APIView):
    #  API view to create a new admin user.
    
        @method_decorator(login_required)
        @permission_required("userData.add_admin")
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
                    return Response(data={"message":"Admin Limit exceeded"} , status=status.HTTP_403_FORBIDDEN)
                serializer.save()
                admin.join_Count -=1
                return Response(data={
        "message":"Created Admin"}, status= status.HTTP_201_CREATED)
            return Response( serializer.errors , status= status.HTTP_400_BAD_REQUEST)


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
            
            serializer = UserSerializer(data=request.data , context = {"employee":request.data["employee"]})
            if serializer.is_valid():
                data_Object = serializer.save()
                print(int(data_Object["pk"]))
                response= requests.post(url=request.build_absolute_uri(reverse(viewname= "email_Service" , kwargs=({"pk": int(data_Object["pk"])}) )), data=data_Object)
                return Response(data=response.json() ,status=response.status_code)
            else:    
                return Response( serializer.errors , status= status.HTTP_400_BAD_REQUEST)
        
        @method_decorator(login_required)
        @permission_required("userData.change_user")
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
        
        
class Role_View(APIView):
    #    API view to create, retrieve, update roles.
    @method_decorator(login_required)
    @method_decorator(permission_required(["userData.add_role"]))   
    def post(self , request):
        data = request.data
        print(data ,"Asdf")
        serializer=  RoleSerializer(data=data )
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
        instance = get_object_or_404(Role,pk=pk)
        serializer = RoleSerializer(data=request.data , instance= instance)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"updated succsusful"} , status=status.HTTP_200_OK)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
            
@api_view(["GET"])
@login_required
@permission_required(["userData.view_role"])
def Get_Role(request,pk):
    roles = get_object_or_404(Role,pk=pk)
    serializers =RoleSerializer(roles )
    print(serializers)
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
            serializers=RoleHierarchySerializer(data=roleData , context = {"user" : requestedUser})
            if serializers.is_valid():
                data = serializers.save()
                return Response(data={data["message"]} , status=data["status"])
            return Response(data = serializers.errors ,status=status.HTTP_400_BAD_REQUEST)
        return( Response({"message":"Admin Limit exceeds"} , status=status.HTTP_401_UNAUTHORIZED))

    
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
    def put(self , request,pk):
        
        """
        Handles the PUT request to update a role.
        
        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The primary key of the role to update.

        Returns:
            - JSON response with the updated role data
            - Status code: 200 (OK)
            - JSON response with validation errors
            - Status code: 400 (Bad Request)
        """

        data = request.data
        instance = RoleHierarchy.objects.get(pk=pk)
        serializer =  RoleHierarchySerializer(instance = instance, data=data )
        if serializer.is_valid():
           updated =  serializer.save()
           return Response(data=updated , status=status.HTTP_200_OK)
        return Response(data= serializer.errors ,status=status.HTTP_400_BAD_REQUEST)
    
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
        if child ==0 :
            cur_Role.delete()
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

    
    role_object =get_object_or_404(RoleHierarchy, role=role)    
    available_reporting_roles = role_object.get_ancestors()
    serializer = RoleHierarchySerializer(available_reporting_roles ,)
    print(serializer.data)
    return  serializer.data



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
                response =  requests.post(url=request.build_absolute_uri(reverse(viewname= "create_user" )) , data={
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

    
    emp = get_object_or_404(Employee,pk=pk)
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
        emp.delete()
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