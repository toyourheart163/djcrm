# permission.py
# ————————74PerfectCRM实现CRM权限和权限组限制URL————————
from django.urls import resolve # resolve解析URL
from django.shortcuts import render,redirect,HttpResponse #页面返回
from permissions.permission_list import perm_dic #权限字典

def perm_check(*args,**kwargs):
    print( '执行perm_check：', *args, **kwargs )
    request = args[0]#
    # print(request) #<WSGIRequest: GET '/king_admin/crm/firstlayermenu/4/change/'>

    resolve_url_obj = resolve(request.path)#反解URL路径#获取当前的URL# resolve解析URL#生成实例
    print('反解URL路径:',resolve_url_obj)#ResolverMatch(func=permissions.permission.inner, args=('crm', 'firstlayermenu', '4'), kwargs={}, url_name=table_change, app_names=[], namespaces=[])
    current_url_name = resolve_url_obj.url_name  # 当前url的url_name
    print('当前用户:',request.user,'当前url的url_name:',current_url_name)#admin2 当前url的url_name: table_change

    permission_list= request.user.user_permissions.values_list('codename') # 根据 登陆的ID 获取 拥有的权限列表
    print('拥有的权限列表',permission_list)

    permission_group = request.user.groups.all().values_list('permissions__codename')    # 根据 登陆的ID 获取 拥有的组
    print('拥有的权限组',permission_group)

    match_key = None
    match_results = [False,] #后面会覆盖，加个False是为了让all(match_results)不出错

    for permission_key,permission_val in  perm_dic.items():#从权限字典中取相关字段 #crm_table_index':['1','table_index','GET',[],{},],
        # print('循环权限表',((permission_key),))
        if ((permission_key),) in permission_list or ((permission_key),) in permission_group:#权限列表是元组
            per_url_name = permission_val[0] #URL
            per_method  = permission_val[1] #GET #POST #请求方法
            perm_args = permission_val[2]  # 列表参数
            perm_kwargs = permission_val[3]# 字典参数
            custom_perm_func = None if len(permission_val) == 4 else permission_val[4] #url判断 #自定义权限钩子
            # 'crm_can_access_my_clients':['table_list','GET',[],{'perm_check':33,'arg2':'test'}, custom_perm_logic.only_view_own_customers],
            # print('URL:',per_url_name,'请求方法:',per_method,'列表参数:',perm_args,'字典参数:',perm_kwargs,'自定义权限钩子:',custom_perm_func)


            if per_url_name == current_url_name: #权限字典的 URL  ==当前请求的url #crm_table_index':['URL','请求方法',[列表参数],{字典参数},],
                if per_method == request.method: #权限字典的 请求方法 == 当前请求的方法  #crm_table_index':['URL','请求方法',[列表参数],{字典参数},],
                    #逐个匹配参数，看每个参数时候都能对应的上。
                    args_matched = False #参数匹配 #仅供参数
                    for item in perm_args: #循环列表参数 #crm_table_index':['URL','请求方法',[列表参数],{字典参数},],
                        request_method_func = getattr(request,per_method) #反射 #请求方法 #GET #POST
                        if request_method_func.get(item,None):# 如果request字典中有此参数
                            args_matched = True
                        else:
                            print("参数不匹配......")
                            args_matched = False
                            break  # 有一个参数不能匹配成功，则判定为假，退出该循环。
                    else:
                        args_matched = True #没有执行 break 表示 列表匹配成功 #防止列表没有使用参数时出错

                    #匹配有特定值的参数
                    kwargs_matched = False
                    for k,v in perm_kwargs.items(): #循环字典参数#crm_table_index':['URL','请求方法',[列表参数],{字典参数},],
                        request_method_func = getattr(request, per_method) #反射 #请求方法 #GET #POST
                        arg_val = request_method_func.get(k, None)  # request字典中有此参数
                        print("perm kwargs check:",arg_val,type(arg_val),v,type(v))
                        if arg_val == str(v): #匹配上了特定的参数 及对应的 参数值， 比如，需要request 对象里必须有一个叫 user_id=3的参数
                            kwargs_matched = True
                        else:
                            kwargs_matched = False
                            break # 有一个参数不能匹配成功，则判定为假，退出该循环。
                    else:
                        kwargs_matched = True


                    #自定义权限钩子
                    perm_func_matched = False
                    if custom_perm_func: #如果有定义
                        if custom_perm_func(request,args,kwargs):#def only_view_own_customers(request,*args,**kwargs):
                            perm_func_matched = True
                        else:
                            perm_func_matched = False #使整条权限失效
                            print('自定义权限钩子没有通过',perm_func_matched)
                    else: #没有定义权限钩子，所以默认通过
                        perm_func_matched = True

                    match_results = [args_matched,kwargs_matched,perm_func_matched] #列表
                    print("匹配结果： ", match_results) # [True, True, True]
                    if all(match_results): #都匹配上了 #都返回 True
                        match_key = permission_key # 给 match_key = None 赋值
                        break  #跳出大循环

    if all(match_results): #如果都匹配成功     #'crm_table_index':['table_index','GET',[],{},],
        app_name, *per_name = match_key.split('_') #先给app_name赋一个值，其他的值都给*per_name     'crm_table_index':
        print("权限名：",match_key,'权限：',match_results)#crm_010902_only_view_CourseRecord_POST [True, True, True]
        print('分割：',app_name, *per_name) #  crm 010902 only view CourseRecord POST
        perm_obj = '%s.%s' % (app_name,match_key)#'crm.table_index' #    url(r'^(\w+)/$', views.table_index, name='table_index'),  # 单个具体app页面
        print("生成权限:",perm_obj) #crm.crm_010902_only_view_CourseRecord_POST
        if request.user.has_perm(perm_obj):
            print('当前用户有此权限')
            return True
        else:
            print('当前用户没有该权限')
            return False
    else:
        print("未匹配到权限项，当前用户无权限")

def check_permission(func):
    print('权限func',func)#权限func <function table_data_list at 0x030636A8> #循环 URL name
    def inner(*args,**kwargs):
        print('开始权限匹配：',type(args))
        request = args[0]#请求第一个
        print('判断登陆情况：')
        if request.user.id == None:
            print('未登陆')
            return redirect( '/gbacc/gbacc_login/' )#返回登陆页面
        else:
            if request.user.is_superuser == True:
                print('超级管理员')
                return func( *args, **kwargs )  #直接返回 真
            print( '已登陆,判断有perm_check(*args,**kwargs)去执行' )
            if not perm_check(*args,**kwargs): #如果返回不为真 #没权限
                print('#没权限',perm_check(*args,**kwargs))
                request = args[0]
                return HttpResponse('你没有这个权限')
            print('有权限',func(*args,**kwargs)) #<HttpResponse status_code=200, "text/html; charset=utf-8">
            return func(*args,**kwargs)
    print('inner',inner)
    return  inner #返回 真或假
# ————————74PerfectCRM实现CRM权限和权限组限制URL————————

# permission.py