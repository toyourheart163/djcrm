import json

from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .app_config import kingadmin_auto_discover
from .base_admin import site

kingadmin_auto_discover()

print('site:', site.registered_sites)

# Create your views here.
def app_index(request):
    return render(request, 'king_admin/app_index.html', {'site': site})

def logout(request):
    return redirect('/')

def filter_querysets(request,queryset):
    condtions = {}
    for k,v in request.GET.items():#不需要空的,判断是否为空
        if k in ("page", "_o", "_q"):
            continue
        if v:
            condtions[k] = v
    query_res = queryset.filter(**condtions)
    return query_res,condtions

def table_data_list(request,app_name,model_name):
    #通过2个参数到base_admin里获取class AdminRegisterException(Exception): 的对象
    admin_obj = site.registered_sites[app_name][model_name]  #base_admin
    admin_obj.querysets =  admin_obj.model.objects.all()#取数据 传到 前端
    
    if request.method == 'POST':
        selected_action = request.POST.get('action')
        selected_ids = json.loads(request.POST.get('selected_ids'))
        if not selected_action:
            if selected_ids:
                admin_obj.model.objects.filter(id__in=selected_ids).delete()
        else:
            selected_objs = admin_obj.model.objects.filter(id__in=selected_ids)
            admin_action_func = getattr(admin_obj, selected_action)
            response = admin_action_func(admin_obj, request, admin_obj.model.objects.filter(id__in=selected_ids))
            if response:
                return response

    obj_list =  admin_obj.model.objects.all()#取数据 传到 前端  #base_admin  #获取传过来的所有对象
    queryset, condtions = filter_querysets(request, obj_list)  #base_admin   # 调用条件过滤
    queryset = get_queryset_search_result(request,queryset,admin_obj)##搜索后
    sorted_queryset = get_orderby(request, queryset) 
    paginator = Paginator(sorted_queryset, admin_obj.list_per_page)
    page = request.GET.get('page')
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)
    admin_obj.querysets = objs  # base_admin
    admin_obj.filter_condtions = condtions  # base_admin
    return render(request,"king_admin/table_data_list.html",locals())
# ————————08PerfectCRM实现King_admin显示注册表的字段表头————————

def get_orderby(request,queryset):
    orderby_key = request.GET.get("_o")
    if orderby_key:
        return  queryset.order_by(orderby_key)
    return  queryset

from django.db.models import Q
from  king_admin import forms

def get_queryset_search_result(request,queryset,admin_obj):
    search_key = request.GET.get("_q", "")#取定义名,默认为空
    q_obj = Q()#多条件搜索 #from django.db.models import Q
    q_obj.connector = "OR"  # or/或 条件
    for column in admin_obj.search_fields: #搜索目标crm/kingadmin里class CustomerAdmin(BaseAdmin):search_fields = ('name','qq',)
        q_obj.children.append(("%s__contains" % column, search_key)) #运态添加多个条件
    res = queryset.filter(q_obj) #对数据库进行条件搜索
    return res

def table_change(request,app_name,model_name,obj_id):
    admin_obj = site.registered_sites[app_name][model_name]   #获取表对象
                #kingadmin/forms.py里def CreateModelForm(request,admin_obj):
    model_form = forms.CreateModelForm(request,admin_obj=admin_obj)  ##modelform 生成表单 加验证
    # obj_form = model_form()  # 表单
    obj = admin_obj.model.objects.get(id=obj_id)#根据ID获取数据记录

    # ————————20PerfectCRM实现King_admin数据修改美化————————
    # #面向对象最重要的概念就是类（Class）和实例（Instance），必须牢记类是抽象的模板，比如Student类，而实例是根据类创建出来的一个个具体的“对象”，每个对象都拥有相同的方法，但各自的数据可能不同。
    # obj_form = model_form(instance=obj)  # 数据传入表单

    if request.method == "GET":
        obj_form = model_form(instance=obj)
    elif request.method == "POST":
        obj_form = model_form(instance=obj,data=request.POST)
        if obj_form.is_valid():
            obj_form.save()
    # ————————20PerfectCRM实现King_admin数据修改美化————————

    return render(request,"king_admin/table_change.html",locals())

def table_index(request,app_name):
    bases = site.registered_sites[app_name]#取出对应app对象
    return render(request, 'king_admin/table_index.html', {"site":bases,'app_name':app_name})

from django.shortcuts import redirect  # kingadmin添加内容

def table_add(request,app_name,model_name):
    admin_obj = site.registered_sites[app_name][model_name]  #获取表对象
    model_form = forms.CreateModelForm(request,admin_obj=admin_obj) ##modelform 生成表单 加验证
    if request.method == "GET":
        obj_form = model_form()

    elif request.method == "POST":
        obj_form = model_form(data=request.POST)  #创建数据
        if obj_form.is_valid():
            obj_form.save()
        if not obj_form.errors:   #没有错误返回原来的页面
            #from django.shortcuts import redirect
            return  redirect("/king_admin/%s/%s/" % (app_name,model_name))
    return render(request, "king_admin/table_add.html", locals())

def table_delete(request,app_name,model_name,obj_id):
    admin_obj = site.registered_sites[app_name][model_name]#表类
    objs=admin_obj.model.objects.filter(id=obj_id)#类的对象
    if request.method=='POST':
        objs.delete()#删除
        return redirect("/king_admin/%s/%s/" % (app_name,model_name))#转到列表页面
    return render(request, "king_admin/table_delete.html", locals())#locals 返回一个包含当前范围的局部变量字典。