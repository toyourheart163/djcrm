from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.app_index),
    path('logout/', views.logout),
    re_path(r'^(\w+)/(\w+)/$', views.table_data_list,name='table_data_list'),#详细内容
    re_path(r'^(\w+)/(\w+)/(\d+)/change/$', views.table_change,name='table_change'),
    re_path(r'^(\w+)/$', views.table_index, name='table_index'),
    re_path(r'^(\w+)/(\w+)/add/$', views.table_add,name='table_add'),
    re_path(r'^(\w+)/(\w+)/(\d+)/delete/$', views.table_delete, name="table_delete"),
    re_path(r'^(\w+)/(\w+)/(\d+)/password/$', views.password_reset, name="password_reset"),  # 修改密码
    re_path(r'^(\w+)/(\w+)/password/$', views.password_add, name="password_add"),  # 修改密码跳转到添加
]
