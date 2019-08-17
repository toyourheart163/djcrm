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
]
