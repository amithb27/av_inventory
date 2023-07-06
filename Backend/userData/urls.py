from django.contrib import admin
from django.urls import path 
from userData.views import *
urlpatterns =[

    #employee  API'S
    path("get_all_emp/", get_all_employees, name="get_all_employees"),
    path("get_one_employee/<int:pk>", get_employee, name="get_employee" ),
    path("get_emp_id/",get_employeeId_for_native_users,name="get_employeeId_for_native_users"),
    path('get_emp_with_role/<int:role>' ,get_employees_with_role , name="get_employees_with_role"),
    path('create_emp/<int:role>' ,post_employee , name="post_employee"),
    path('update_emp/<int:role>' ,update_employee , name="update_employee"),
    path('delete_emp/<int:role>' ,delete_admin , name="delete_admin"),
    
    #utility  API'S
    path("template/",Template,name="template" ),
    path("send_email_with_creds/<int:pk>", send_mail_with_login_creds , name="send_mail_with_login_creds"),
    path('send_mail_with_media',send_mail_with_media , name='send_mail_with_media'),
    path('login/',login_user, name="login"),
    path('logout/',logout_user, name="logout "),
    
    #role  API'S
    path('get_all_role/', get_all_roles, name = "get_all_roles"),
    path('get_all_senior_roles/<str:role>', get_all_senior_roles , name="get_all_senior_roles"),
    path('get_one_role/<int:pk>', get_role, name = "get_role"),
    path('update_role/<int:pk>/update', update_role , name = "update_role"),
    path('create_role/',post_role , name = "post_role"),
    path('delete_role/', delete_role, name = "delete_role"),
    
    #role hierarchy  API'S
    path('get_all_hierarchy_tree/', get_all_hierarchy_tree , name="get_all_hierarchy_tree" ),
    path('update_role_hierarchy/<int:pk>' , update_role_hierarchy , name ="update_role_hierarchy"),
    path('create_role_hierarchy/' , post_rolehierarchy , name ="post_rolehierarchy"),
    path('delete_role_hierarchy/<str:role>' , delete_role_hierarchy, name ="delete_role_hierarchy"),
    
    #user API's
    path( "create_user/ ",post_user,  name="create_user"),
    path('forget_password/' , forgot_user_password , name="forgot_user_password"),
    path('change_password',change_user_password , name="change_user_password"),
    path( "delete_user/ ",post_user,  name="create_user"),

    # admin API's
    path("create_admin/" , post_admin, name="create_admin"),
    path("delete__admin/" , delete_admin, name="create_admin"),
    
    #Permissions API's
    path("get_all_user_perms/",get_user_permissions ,name="get_user_permissions"),
    path("create_permission/",post_permission ,name="post_permission"),
    
    # Product API's
    path('get_all_product/', get_all_products ,name="get_all_products"),
    path('create_product/', post_product ,name="post_product"),
    
    # Brands API's
    path('get_all_brands', get_all_brands,name="get_all_brands"),
    path('create_brand/', post_brand,name="post_brand"),
    
    #Sizes API's
    path('get_all_sizes/', get_all_sizes,name="get_all_sizes"),
    path('create_size/', post_size,name="post_sizes"),
    
    #Category API's
    path('get_all_categories/', get_all_categories,name="get_all_categories"),
    path('create_category', post_category,name="post_size"),
    
    #Units API's
    path('get_all_units', get_all_units,name="get_all_units"),
    path('create_unit', post_unit,name="post_unit"),
    
]