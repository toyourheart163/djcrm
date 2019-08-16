from django.urls import path

from . import auth_views, crm_views

urlpatterns = [
    path('auth_user/', auth_views.auth_user), #Django账号表
    path('crm_Role/', crm_views.crm_Role), #角色表 等基本信息
    path('crm_UserProfile/', crm_views.crm_UserProfile),#账号表 #随机学生
    path('crm_userprofile_roles/', crm_views.crm_userprofile_roles),#账号角色关联表 #随机学生
    path('crm_Customer/', crm_views.crm_Customer),  # 04客户信息表
]
