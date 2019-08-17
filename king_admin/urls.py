from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.app_index),
    path('logout/', views.logout),
    re_path(r'^(\w+)/(\w+)/$', views.table_data_list,name='table_data_list'),#详细内容
]
