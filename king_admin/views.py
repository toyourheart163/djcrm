import json

from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from  django.contrib.auth.decorators import login_required

from .app_config import kingadmin_auto_discover
from .base_admin import site
from  king_admin import forms

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
    
@login_required
def table_data_list(request,app_name,model_name):
    #通过2个参数到base_admin里获取class AdminRegisterException(Exception): 的对象
    admin_obj = site.registered_sites[app_name][model_name]  #base_admin
    if request.method == 'POST':               #分发Django admin的action操作
        action = request.POST.get('action')
        selected_ids = json.loads(request.POST.get('selected_ids'))
        # selected_ids = request.POST.get('selected_ids')
        if not action:
            if selected_ids:
                admin_obj.model.objects.filter(id__in=selected_ids).delete()
        else:
            selected_objs = admin_obj.model.objects.filter(id__in=selected_ids)
            admin_action_func = getattr(admin_obj, action)
            response = admin_action_func(admin_obj, request, selected_objs)
            if response:
                return response

    admin_obj.querysets =  admin_obj.model.objects.all()#取数据 传到 前端
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

def get_queryset_search_result(request,queryset,admin_obj):
    search_key = request.GET.get("_q", "")#取定义名,默认为空
    q_obj = Q()#多条件搜索 #from django.db.models import Q
    q_obj.connector = "OR"  # or/或 条件
    for column in admin_obj.search_fields: #搜索目标crm/kingadmin里class CustomerAdmin(BaseAdmin):search_fields = ('name','qq',)
        q_obj.children.append(("%s__contains" % column, search_key)) #运态添加多个条件
    res = queryset.filter(q_obj) #对数据库进行条件搜索
    return res

@login_required
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

@login_required
def table_index(request,app_name):
    bases = site.registered_sites[app_name]#取出对应app对象
    return render(request, 'king_admin/table_index.html', {"site":bases,'app_name':app_name})

@login_required
def table_add(request,app_name,model_name):
    admin_obj = site.registered_sites[app_name][model_name]  #获取表对象
    model_form = forms.CreateModelForm(request,admin_obj=admin_obj) ##modelform 生成表单 加验证
    if request.method == "GET":
        obj_form = model_form()

    elif request.method == "POST":
        password=request.POST.get('password') #取前端输入的密码
        email=request.POST.get('email') #取前端输入的邮箱
        
        obj_form = model_form(data=request.POST)  #创建数据
        if obj_form.is_valid():
            obj_form.save()

        if not obj_form.errors:   #没有错误返回原来的页面
            #from django.shortcuts import redirect
            if email:
                obj=admin_obj.model.objects.filter(email=email).first()  # 对象
                obj.set_password(password)  # 加密
            try:
                obj.save()#表单验证通过保存
            except Exception as e:
                return redirect("/king_admin/%s/%s/" % (app_name, model_name))
            return  redirect("/king_admin/%s/%s/" % (app_name,model_name))
    return render(request, "king_admin/table_add.html", locals())

@login_required
def table_delete(request,app_name,model_name,obj_id):
    admin_obj = site.registered_sites[app_name][model_name]#表类
    objs=admin_obj.model.objects.filter(id=obj_id)#类的对象
    app_name=app_name
    if admin_obj.readonly_table:
        errors={'锁定的表单':'该表单:<%s>,已经锁定,不能删除当前记录!'%model_name}
    else:
        errors={}
    if request.method=='POST':
        objs.delete()#删除
        return redirect("/king_admin/%s/%s/" % (app_name,model_name))#转到列表页面
    return render(request, "king_admin/table_delete.html", locals())#locals 返回一个包含当前范围的局部变量字典。

@login_required
def password_reset(request,app_name,model_name,obj_id):
    admin_obj = site.registered_sites[app_name][model_name]#表类
    model_form = forms.CreateModelForm(request,admin_obj=admin_obj)#modelform 生成表单 加验证
    obj=admin_obj.model.objects.get(id=obj_id)#类表的对象
    errors={}#错误提示
    if request.method=='POST':
        _password1=request.POST.get('password1')  #获取页面输入的值
        _password2=request.POST.get('password2')  #获取页面输入的值
        if _password1==_password2:
            if len(_password1)>5:
                obj.set_password(_password1)#继承Django方法 #加密
                obj.save()   #保存
                return redirect(request.path.rstrip('password/') + ('/change/'))  #替换URL名
            else:
                errors['password_too_short']='必须不少于6字符'
        else:
            errors['invalid_password']='两次输入的密码不一样'#密码不一致
    return render(request, "king_admin/password_reset.html", locals())

@login_required
def password_add(request,app_name,model_name):
    return redirect("/king_admin/%s/%s/add/" % (app_name, model_name))