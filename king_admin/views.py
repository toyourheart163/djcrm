from django.shortcuts import render, redirect

from .app_config import kingadmin_auto_discover
from .base_admin import site

kingadmin_auto_discover()

print('site:', site.registered_sites)

# Create your views here.
def app_index(request):
    return render(request, 'king_admin/app_index.html', {'site': site})

def logout(request):
    return redirect('/')

def table_data_list(request,app_name,model_name):
    #通过2个参数到base_admin里获取class AdminRegisterException(Exception): 的对象
    admin_obj = site.registered_sites[app_name][model_name]  #base_admin

    admin_obj.querysets =  admin_obj.model.objects.all()#取数据 传到 前端
    return render(request,"king_admin/table_data_list.html",locals())
