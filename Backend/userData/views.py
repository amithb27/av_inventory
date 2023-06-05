from django.shortcuts import  get_object_or_404
from django.urls import reverse
from django.shortcuts import render
from django.core.mail import send_mail
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
from .serializers import *
from django.contrib.auth.decorators import permission_required
from django.utils import timezone
# Create your views here.


@api_view(["POST"])
def SendMail(request):
    print(settings.EMAIL_HOST_USER)
    try  :
        send_mail(
    subject ="Email_testing",
    message= "...Analytics Valley...",
    from_email=settings.EMAIL_HOST_USER,
    recipient_list=["manikantatez@gmail.com"],
    fail_silently=False,
        ) 
        return Response(data={
            "message":"Email sent" 
        }, status=status.HTTP_200_OK )
    except  SMTPException  as e:
        return Response(data={
            "message":e 
        }, status=status.HTTP_400_BAD_REQUEST)

def Template(request):
    my_date = timezone.now()
    month = my_date.strftime("%B" ) +" - "+ my_date.strftime("%d" )
    context={
        "name" :"employee",
        "age" : 20,
        "birthdate":month
    }
    
    return render(request=request , template_name="birthday.html", context=context)

@api_view(["POST"])
def Login(request):
    requestedUser = request.data.username
    password = request.data.password
    user = authenticate(request, username = requestedUser , password = password)   
    if user is not None :
        login(request)
    return Response(data="cannot login with the provided credentials " ,status=status.HTTP_401_UNAUTHORIZED)

@api_view(["GET"])
def Logout(request):
    logout(request)
    return Response(data={
        "message":"logout success"}, status=status.HTTP_200_OK)

class Create_Admin(APIView):
        @method_decorator(login_required)
        @permission_required("userData.add_admin")
        def post(self,request): 
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
        @method_decorator(login_required)
        @permission_required("userData.add_user")
        def post(self,request):
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data={
        "message":"Created User"}, status= status.HTTP_201_CREATED)
            return Response( serializer.errors , status= status.HTTP_400_BAD_REQUEST)
        
        @method_decorator(login_required)
        @permission_required("userData.change_user")
        def patch(self ,request ):
            requested_User = request.user
            serializer =  UserSerializer(data=request.data , instance=requested_User ) 
            if serializer.is_valid():
                serializer.save()
                return Response(data={"message":"Password changed "} ,status=status.HTTP_200_OK)
            return Response(data=serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        

class create_role(APIView):
    # User validations request.user.is_validuser
    @method_decorator(permission_required("userData.add_rolehierarchy"))
    @method_decorator(login_required)  
    def post(self,request):
        roleData=request.data  
        serializers=RoleHierarchySerializer(data=roleData)
        if serializers.is_valid():
            serializers.save()
            return Response (status=status.HTTP_201_CREATED)
        return Response(data = serializers.errors ,status=status.HTTP_400_BAD_REQUEST)
    
    
    @method_decorator(login_required)
    @method_decorator(permission_required("userData.view_rolehierarchy")) 
    def get(self,request,role):
        role_object =get_object_or_404(RoleHierarchy, name=role)    
        available_reporting_roles = role_object.get_ancestors()
        serializer = RoleHierarchySerializer(available_reporting_roles , )
        print(serializer.data)
        return  serializer.data
    
    @method_decorator(login_required)
    @method_decorator(permission_required("userData.view_rolehierarchy"))
    def get(self,request): 
        available_roles = RoleHierarchy.objects.all()
        print(available_roles)
        serializedData = RoleHierarchySerializer(available_roles , many=True)
        return Response(serializedData.data)
    
    @method_decorator(login_required)
    @method_decorator(permission_required("userData.change_rolehierarchy") )
    def put(self , request,pk):
        data = request.data
        instance = RoleHierarchy.objects.get(pk=pk)
        serializer =  RoleHierarchySerializer(instance = instance, data=data )
        if serializer.is_valid():
           updated =  serializer.save()
           return Response(data=updated , status=status.HTTP_200_OK)
        return Response(data= serializer.errors ,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'POST'])
@login_required
@permission_required("userData.change_employee")
def Employees_List(request):
    print(request.session.session_key,"rhiss is session")
    print(user.objects.make_random_password())
    requestedUser = request.user
    
    if request.method == 'GET':
        
        dummy = request.build_absolute_uri(reverse(viewname="create_user" ))
        print(dummy)
        data = Employee.objects.all()
        serializer = EmployeeSerializer(data, many=True)
        return Response(serializer.data ,status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        if requestedUser.join_Count <=0 :
            serializer = EmployeeSerializer(data=request.data ,context = {"requestedUser" : requestedUser})
            if serializer.is_valid():
                (pk,email) = serializer.save()
                is_Web_user = request.data.web_user
                if is_Web_user :
                     return requests.post(url=request.build_absolute_uri(reverse(viewname= "create_user" )) , data={
                        "email" :email,
                        "pk" : pk
                     })
                return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data = {"error":"You exceeded your count limit "} ,status=status.HTTP_401_UNAUTHORIZED)

@login_required
@api_view(['PUT', 'DELETE','GET'])
@permission_required("userData.change_employee")

def Employees_Details(request, pk):
    emp = get_object_or_404(Employee,pk=pk)
    if request.method == 'PUT':
        serializer = EmployeeSerializer(emp, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        emp.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'GET':
        data=EmployeeSerializer(emp)
        return Response(data.data , status=status.HTTP_302_FOUND)