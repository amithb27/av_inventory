from django.shortcuts import render , get_object_or_404
from rest_framework.response import Response
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.decorators import api_view 
from rest_framework.views import APIView
from rest_framework import status 
from .models import *
from .serializers import *
from django.contrib.auth.decorators import permission_required
# Create your views here.

class Create_Groups(APIView) :
    def post(self,request,name):
     try :   
        group = Group.objects.get(name=name)
        return Response(status=status.HTTP_226_IM_USED)
     except Group.DoesNotExist:
         Group.objects.create(name=name)


class Create_User(APIView):

    def post(self,request,type):
        serializer = UserSerializer(data=request.data ,context ={"type":type} )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer, status= status.HTTP_201_CREATED)
        return Response(serializer.errors , status= status)
            


class create_role(APIView):
    # User validations request.user.is_validuser
        
    def post(self,request):
        roleData=request.data  
        serializers=RoleHierarchySerializer(data=roleData)
        if serializers.is_valid():
            serializers.save()
            return Response (status=status.HTTP_201_CREATED)
        return Response( serializers.errors ,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,role):
        role_object =get_object_or_404(RoleHierarchy, name=role)    
        available_reporting_roles = role_object.get_ancestors()
        serializer = RoleHierarchySerializer(available_reporting_roles , )
        print(serializer.data)
        return  serializer.data
    
    def get(self,request): 
        available_roles = RoleHierarchy.objects.all()
        print(available_roles)
        serializedData = RoleHierarchySerializer(available_roles , many=True)
        return Response(serializedData.data)
    def update(self , request,pk):
        data = request.data
        instance = RoleHierarchy.objects.get(pk=pk)
        serializer =  RoleHierarchySerializer(instance = instance, data=data )
        if serializer.is_valid():
           updated =  serializer.save()
           return Response(data=updated , status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
def templateView(request):
    return render(request,"index.html")

@api_view(['GET', 'POST'])
def Employees_List(request):
    requestedUser = request.user.username
    if request.method == 'GET':
        
        data = Employee.objects.all()

        serializer = EmployeeSerializer(data, many=True)
       
        return Response(serializer.data ,status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        print(request.data, "usernamee")
        if requestedUser.join_Count <=0 :
            serializer = EmployeeSerializer(data=request.data ,context = {"requestedUser" ,requestedUser})
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data = {"error":"You exceeded your count limit "} ,status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PUT', 'DELETE','GET'])
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