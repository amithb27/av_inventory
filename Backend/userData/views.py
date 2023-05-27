from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view 
from rest_framework import status 
from .models import *
from .serializers import *
# Create your views here.


@api_view(['POST',"GET"])
def create_role(request):
    #   user validations request.user.is_validuser
    roleData=request.data
    
    if request.method == "POST":
         serializers=RoleHierarchySerializer(data=roleData)
         if serializers.is_valid():
             return Response (status=status.HTTP_201_CREATED)
         return Response( serializers.errors ,status=status.HTTP_400_BAD_REQUEST)
    
        
    if request.method == "GET":
        available_roles = RoleHierarchy.objects.all()
        print(available_roles)
        serializedData = RoleHierarchySerializer(available_roles , many=True)
        return Response( serializedData.data)
        
    





@api_view(['GET', 'POST'])
def Employees_List(request):
    if request.method == 'GET':
        
        data = Employee.objects.all()
  
        serializer = EmployeeSerializer(data, context={'request': request}, many=True)
       
        return Response(serializer.data)

    elif request.method == 'POST':
        print(request.data, "usernamee")
        
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        print(serializer.errors , "eoors are here")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT', 'DELETE','GET'])
def Employees_Details(request, pk):
    try:
        emp = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

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
        return Response(data.data)