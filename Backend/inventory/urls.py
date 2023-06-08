"""inventory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path 
from userData.views import *
urlpatterns = [

    path("temp/",Template,name="Temp"),
    path('admin/', admin.site.urls),
    path("employee/", Employees_List, name="employee_list"),
    path("employee/<int:pk>", Employees_Details, name="employee_list" ),
    path('role/', create_role.as_view() , name="create_role" ),
    path('role/<str:role>', create_role.as_view() , name="reporting_role_callback "),
    path('role/<int:pk>', create_role.as_view() , name="reporting_role_callback "),
    path('login/', Login , name="Login "),
    path('logout/', Logout, name="Logout "),
    path( "user/ ",Create_User.as_view() ,  name="create_user"),
    path("admin/" , Create_Admin.as_view(), name="create_admin"),
    path("email/<int:pk>", SendMail , name="email_Service"),
    path("permissions/<int:pk>",Employee_Permission.as_view() ,name="permission"),
    path("profile/",MobileProfile,name="profile")
]
