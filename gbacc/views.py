# gbacc_views.py
# ————————38PerfectCRM实现全局账号登录注销————————
from django.contrib.auth import login #记录登录 #Django在数据库创建一条记录 #记住密码，免登录
from django.contrib.auth import authenticate #调用用户认证模块
from django.contrib.auth import logout #注销功能
from django.shortcuts import render  #页面返回
from django.shortcuts import redirect  #页面返回

# ————————39PerfectCRM实现登录+验证码+过期时间+页面保留账号————————
#验证码函数 #处理注册的内容
from io import BytesIO #创建内存空间
from django.shortcuts import HttpResponse #页面返回
from gbacc.gbacc_auxiliary.check_code import create_validate_code #验证图片
def check_code(request):
    stream = BytesIO()#创建内存空间
    img, code = create_validate_code()#调用验证码图片生成函数 返回图片 和 对应的验证码
    img.save(stream, 'PNG')#保存为PNG格式
    request.session['CheckCode'] = code#保存在session中
    return HttpResponse(stream.getvalue())
# ————————39PerfectCRM实现登录+验证码+过期时间+页面保留账号————————

#全局账号登录
def gbacc_login(request):

    # ————————39PerfectCRM实现登录+验证码+过期时间+页面保留账号————————
    email={} #变字典#传前端#页面获取值
    _email = request.POST.get('email')  #关键语句 #获取前端输入的值
    request.session['email'] = _email  #保存到 session 里
    email=request.session.get('email')   #保存到变量#变字典#传前端
    import datetime
    today_str = datetime.date.today().strftime("%Y%m%d")   #获取时间#登陆过期
    # ————————39PerfectCRM实现登录+验证码+过期时间+页面保留账号————————
    
    errors={}
    if request.method =="POST":
        _email=request.POST.get('email')
        _password=request.POST.get('password')
        # ————————39PerfectCRM实现登录+验证码+过期时间+页面保留账号————————
        #后台生成的验证码#调用上面def check_code(request):        #页面输入的验证码
        if request.session.get('CheckCode').upper() == request.POST.get('check_code').upper():#验证码
        # ————————39PerfectCRM实现登录+验证码+过期时间+页面保留账号————————
            user =authenticate(username=_email,password=_password)#调用用户认证模块
            print('认证账号密码',user)
            if user:
                login(request,user)#记录登录 #Django在数据库创建一条记录 #记住密码，免登录
                # ————————39PerfectCRM实现登录+验证码+过期时间+页面保留账号————————
                request.session.set_expiry(60*60)  #登陆过期时间
                # ————————39PerfectCRM实现登录+验证码+过期时间+页面保留账号————————
                next_url =request.GET.get('next','/')#跳转的页面,默认为首页
                return redirect(next_url)
            else:
                errors['error']='认证失败!'
        # ————————39PerfectCRM实现登录+验证码+过期时间+页面保留账号————————
        else:
            errors['error']= "验证码错误!"
        # ————————39PerfectCRM实现登录+验证码+过期时间+页面保留账号————————
    return render(request,'gbacc_specific/gbacc_login.html',locals())

#全局账号注销
def gbacc_logout(request):
    logout(request)  #调用Djangao 注销功能
    return redirect('/gbacc/gbacc_login/')
# ————————38PerfectCRM实现全局账号登录注销————————


# ————————40PerfectCRM实现全局账号注册+验证码+页面刷新保留信息————————
# json 对错误信息对象进行处理 #处理注册的内容
import json  # 转为json格式
from django.core.exceptions import ValidationError  # 错误信息
class JsonCustomEncoder(json.JSONEncoder):
    def default(self, field):
        if isinstance(field, ValidationError):  # 如果是错误信息进行处理
            return {'code': field.code, 'messages': field.messages}
        else:
            return json.JSONEncoder.default(self, field)

# 注册
from gbacc.gbacc_auxiliary.account import RegisterForm  # 注册验证
from django.contrib.auth.hashers import make_password  # 密码加密
from crm import models   #数据库

def gbacc_register(request):
    email = {}  #页面刷新保留信息
    _email = request.POST.get('email')  # 关键语句 #获取前端输入的值
    request.session['email'] = _email  # 保存到 session 里
    email = request.session.get('email')  # 保存到变量#变字典#传前端

    name = {} #页面刷新保留信息
    _name = request.POST.get('name')  # 关键语句 #获取前端输入的值
    request.session['name'] = _name  # 保存到 session 里
    name = request.session.get('name')  # 保存到变量#变字典#传前端

    password = {} #页面刷新保留信息
    _password = request.POST.get('password') # 关键语句 #获取前端输入的值
    request.session['password'] = _password  # 保存到 session 里
    password = request.session.get('password')  # 保存到变量#变字典#传前端

    errors = {}  #错误信息
    if request.method == 'POST':
        obj = RegisterForm(request=request, data=request.POST)  # 注册验证 #PerfectCRM.gbacc_auxiliary.account
        if obj.is_valid(): #如果表单没有错误，则返回true。否则为假。如果错误是被忽略，返回false。
            name = obj.cleaned_data.get('name')  # 获取用户名
            password = obj.cleaned_data.get('password')  # 获取密码
            email = obj.cleaned_data.get('email')  # 获取邮箱账号
            password = make_password(password, )  # 对密码进行加密
            # ——————数据库添加数据——————
            models.UserProfile.objects.create(name=name, password=password, email=email, )
            # ——————数据库添加数据——————
            # ——————注册后自动登录——————
            import datetime
            today_str = datetime.date.today().strftime("%Y%m%d")  # 获取时间#登陆过期
            user =authenticate(username=_email,password=_password)#调用用户认证模块
            if user:
                login(request,user)#记录登录 #Django在数据库创建一条记录 #记住密码，免登录
                request.session.set_expiry(60*60)  #登陆过期时间
                next_url =request.GET.get('next','/')#跳转的页面,默认为首页
                return redirect(next_url)
            else:
                errors ='认证失败!走到这请联系告诉我。。。'
            # ——————注册后自动登录——————
        else:
            errors = obj.errors.as_data()  #获取全部 account.py 处理的不同错误信息 #到页面显示{{ errors.name.0 }}
    return render(request, 'gbacc_specific/gbacc_register.html', locals())
# ————————40PerfectCRM实现全局账号注册+验证码+页面刷新保留信息————————

from king_admin import base_admin  # king_admin/base_admin.py
from  king_admin import forms as kingforms  #king_admin/forms.py

def gbacc_modify(request,user_id):#用户密码修改
    admin_obj = base_admin.site.registered_sites['crm']['userprofile']#表类
    model_form = kingforms.CreateModelForm(request,admin_obj=admin_obj)#modelform 生成表单 加验证
    obj=admin_obj.model.objects.get(id=user_id)#类表的对象
    errors={}#错误提示
    if request.method=='POST':
        _password0=request.POST.get('password0')
        user =authenticate(username=obj.email,password=_password0)#调用用户认证模块
        print('obj.email',obj.email)
        print('验证比对数据库',user)
        _password1=request.POST.get('password1')
        _password2=request.POST.get('password2')
        if user:
            if _password1==_password2:
                if len(_password1)>5:
                    obj.set_password(_password1)#继承Django方法 #加密
                    obj.save()
                    return redirect('/gbacc/gbacc_login/')
                else:
                    errors['password_too_short']='密码必须不少于6字符'
            else:
                errors['invalid_password']='两次输入的密码不一样'
        else:
            errors['original_password'] = '原密码错误'
    return render(request,'gbacc_specific/gbacc_modify.html',locals())
# ————————41PerfectCRM实现全局账号密码修改————————
# gbacc_views.py