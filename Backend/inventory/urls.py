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
    path('rolehierarchy/', RoleHierarchy_View.as_view() , name="create_role" ),
    path('rolehierarchy/<str:role>', GetRoleNode , name="reporting_role_callback"),
    path('rolehierarchy/<int:pk>' , RoleHierarchy_View.as_view() , name ="updateHyrarchy"),
    path('role/', Role_View.as_view() , name = "roles"),
    path('role/<int:pk>', Get_Role , name = "get_roles"),
    path('role/<int:pk>/update', Role_View.as_view() , name = "get_roles"),
    path('login/', Login , name="Login "),
    path('logout/', Logout, name="Logout "),
    path( "user/ ",Create_User.as_view() ,  name="create_user"),
    path("makeAdmin/" , Create_Admin.as_view(), name="create_admin"),
    path("email/<int:pk>", SendMail , name="email_Service"),
    path("permissions/<int:pk>",Employee_Permission.as_view() ,name="permission"),
    path("mobileApp/",MobileProfile,name="profile"),
    path('forgetPassword/' , ForgetPassword , name="forgetPassword"),
    path('restPassword',ResetPassword , name="restPassword"),
    path('triggerMail',TriggerMail , name='triggerMail'),
    
]
