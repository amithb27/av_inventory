from django.contrib import admin
from django.urls import path 
from userData.views import *


urlpatterns =[
    path("temp/",Template,name="Temp" ),
    path('admin/', admin.site.urls),
    path("employee/", get_all_employees, name="employee_list"),
    path("employee/<int:pk>", get_employee, name="employee_list" ),
    path('rolehierarchy/', get_all_hierarchy_tree , name="create_role" ),
    path('rolehierarchy/<str:role>', get_all_senior_roles , name="reporting_role_callback"),
    path('rolehierarchy/<int:pk>' , update_role_hierarchy , name ="updateHyrarchy"),
    path('role/', get_all_roles, name = "roles"),
    path('role/<int:pk>', get_role, name = "get_roles"),
    path('role/<int:pk>/update', update_role , name = "get_roles"),
    path('login/',login_user, name="Login "),
    path('logout/',logout_user, name="Logout "),
    path( "user/ ",post_user,  name="create_user"),
    path("makeAdmin/" , post_admin, name="create_admin"),
    path("email/<int:pk>", send_mail_with_login_creds , name="email_Service"),
    path("permissions/",get_user_permissions ,name="permission"),
    path("mobileApp/",get_employeeId_for_native_users,name="profile"),
    path('forgetPassword/' , forgot_user_password , name="forgetPassword"),
    path('restPassword',change_user_password , name="restPassword"),
    path('triggerMail',send_mail_with_media , name='triggerMail'),
    path('getempwithRole/<int:role>' ,get_employees_with_role , name="GetEmployeeWithRole"),
    path('product/', get_all_products),
    path('brand/', post_product),
    path('brand/', get_all_brands),
    path('brand/', post_brand),
    path('size/', get_all_sizes),
    path('brand/', post_size),
    path('cetegory/', get_all_categories),
    path('brand/', post_category),
    path('unit/', get_all_units),
    path('brand/', post_unit),
]