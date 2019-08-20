# gbacc_ajax_views.py
# ————————42PerfectCRM实现AJAX全局账号注册————————
from django.shortcuts import render  #页面返回
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
# json 对错误信息对象进行处理 #处理注册的内容
import json  # 转为json格式
from django.core.exceptions import ValidationError  # 错误信息
class JsonCustomEncoder(json.JSONEncoder):
    def default(self, field):
        if isinstance(field, ValidationError):  # 如果是错误信息进行处理
            return {'code': field.code, 'messages': field.messages}
        else:
            return json.JSONEncoder.default(self, field)
# AJAX注册
from gbacc.gbacc_auxiliary.account import RegisterForm  # 注册验证
from django.contrib.auth.hashers import make_password  # 密码加密
from crm import models   #数据库
def gbacc_ajax_register(request):
    if request.method=='GET':
        obj=RegisterForm(request=request, data=request.POST) #注册验证 #PerfectCRM.gbacc_auxiliary.account
        return render(request, 'gbacc_ajax/gbacc_ajax_register.html',{'obj':obj})
    elif request.method=='POST':
        #返回的字符串 字典
        ret={'status':False,'error':None,'data':None}
        #进行验证 调用RegisterForm
        obj=RegisterForm(request=request, data=request.POST)#注册验证 #PerfectCRM.gbacc_auxiliary.account
        if obj.is_valid():
            name = obj.cleaned_data.get('name')#获取用户名
            pwd = obj.cleaned_data.get('password')    #获取密码
            email= obj.cleaned_data.get('email')  #获取邮箱账号
            password=make_password(pwd,)#密码加密
            #print(username,password,email)
            #——————数据库添加数据——————
            models.UserProfile.objects.create(name=name,password=password,email=email,)
            #——————数据库添加数据——————

            #——————获取用户数据，放进个人主页——————
            # user_info= models.UserProfile.objects. \
            #     filter(email=email, password=password). \
            #     values('id', 'name', 'email',).first()
                # #nid=user_info.id
            # print(user_info,type(user_info),'..........')
                # admin_obj = base_admin.site.registered_sites['crm']['userprofile']#表类
                # user_obj=admin_obj.model.objects.get(id=user_info['id'])#类表的对象
                # user_obj.set_password(password)#加密
                # user_obj.save()
            # request.session['user_info'] = user_info   # session
                #print(user_info.id)
            #——————获取用户数据，放进个人主页——————
            #——————AJAX if (arg.status) { #状态——————
            ret['status']=True  #状态
            ret['data']=obj.cleaned_data
            # print(obj.cleaned_data)
            # print(ret)
            #对错误信息对象进行转化处理 前端不用二次序列化
            ret=json.dumps(ret)#转为json格式
            #return HttpResponse(ret)
            #——————AJAX if (arg.status) { #状态——————
        else:
            #加入错误信息
                #print(obj.errors)
            ret['error']=obj.errors.as_data()
            #提示为False
                #ret['status']=False
            #对错误信息对象进行转化处理 前端不用二次序列化
            ret=json.dumps(ret,cls=JsonCustomEncoder)  #转为json格式
                #print(ret)
        return HttpResponse(ret)
# ————————42PerfectCRM实现AJAX全局账号注册————————


# ————————43PerfectCRM实现AJAX全局账号登陆————————
from django.contrib.auth import login #记录登录 #Django在数据库创建一条记录 #记住密码，免登录
from django.contrib.auth import authenticate #调用用户认证模块
#全局账号登录
def gbacc_ajax_login(request):
    if request.method=='GET':
        next_url = request.GET.get("next")
        if not next_url:
            next_url='/'
        request.session['next_url']=next_url
        return render(request, 'gbacc_ajax/gbacc_ajax_login.html', locals())
    elif request.method =="POST":
        ret = {'status': False, 'usererror': None,'chederror': None, 'data': None,'next_url':None}
        _email=request.POST.get('email')
        _password=request.POST.get('password')
        if request.session.get('CheckCode').upper() == request.POST.get('check_code').upper():
            user =authenticate(username=_email,password=_password,)#调用用户认证模块
            print('认证账号密码',user)
            if user:
                login(request,user)#记录登录 #Django在数据库创建一条记录 #记住密码，免登录.
                # next_url= request.GET.get("next",'/')
                ret['status'] = True  # 状态
                ret['next_url'] = request.session.get('next_url')
                ret = json.dumps(ret, cls=JsonCustomEncoder) # 转为json格式
            else:
                ret['usererror']='账号或者密码错误!'
                # 对错误信息对象进行转化处理 前端不用二次序列化
                ret = json.dumps(ret, cls=JsonCustomEncoder)
        else:
            ret['chederror'] = '验证码错误!'
            #对错误信息对象进行转化处理 前端不用二次序列化
            ret=json.dumps(ret,cls=JsonCustomEncoder)
        return HttpResponse(ret)
# ————————43PerfectCRM实现AJAX全局账号登陆————————


# ————————44PerfectCRM实现账号快速注册登陆————————
from django.core.mail import send_mail
# send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
import random
#发送邮件的功能 #验证码#密码
class stmp() :
    def __init__(self):
        self.nowTime=None  #现在的时间
        self.oldTime=None  #过期的时间
        self.emaillist=[]  #发送给谁
        self.code=None    #验证码#密码
    def stmps(self,request,email): #传参数#页面，session #邮箱，发送给谁
        self.emaillist.append(email) #将邮箱地址添加到调用Django发送邮件功能
        # ——————生成发送的时间,用来过期时间——————
        Time = datetime.datetime.now()  #现在的时间
        self.oldTime = Time + datetime.timedelta(seconds=60)  # 设置验证码过期时间 #现在的时间加上设置的参数等于过期时间
        self.oldTime = self.oldTime.strftime('%Y-%m-%d %H:%M:%S')  # 格式化时间
        request.session['oldTime'] = self.oldTime  # 将过期时间放进session进行对比
        # ——————生成发送的时间,用来过期时间——————
        # ——————生成验证码——————
        _letter_cases = "abcdefghjkmnpqrstuvwxy"  # 小写字母，去除可能干扰的i，l，o，z
        _upper_cases = _letter_cases.upper()  # 大写字母
        _numbers = ''.join(map(str, range(3, 10)))  # 数字
        chars = ''.join((_letter_cases, _upper_cases, _numbers))  # 变成一条字符串
        list = random.sample(chars, 4)  # 从一条字符串随机选4个字符变成列表
        self.code = ''.join(list)  # 列表变字符串
        request.session['check_smtp'] = self.code   # 将验证码放进session进行对比#邮件内容
        # ——————生成验证码——————
        # ——————调用Django发送邮件——————
        title= 'PerfectCRM项目自动邮件：%s'%self.code   # 邮件标题#防止一样的内容被邮箱屏蔽
        send_mail(title,  # 邮件标题
                  self.code,  # 验证码内容
                  'perfectcrm@sina.cn',  # 发送的邮箱  #根据情况重新配置
                  self.emaillist,  # 接受的邮箱
                  fail_silently=False,  # 静默,抛出异常
                  )
        print('发送邮件成功！没收到要换标题！检查发送邮箱的配置！')
        # ——————调用Django发送邮件——————
    def nowtime(self):  #现在的时间
        self.nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 格式化时间
        return self.nowTime #返回格式化后的时间
# ————————44PerfectCRM实现账号快速注册登陆————————

# ————————44PerfectCRM实现账号快速注册登陆————————
import datetime  # 获取时间#登陆过期
from django.shortcuts import redirect  #页面返回
# from django.contrib.auth import login  # 记录登录 #Django在数据库创建一条记录 #记住密码，免登录
# from django.contrib.auth import authenticate  # 调用用户认证模块
def gbacc_fast_login(request):
    email = request.POST.get('email')  # 让页面POST提交的值，在页面GET后仍然存在显示
    _email = request.session.get('email')   # 查询session 里
    if not _email:
        request.session['email'] = email  # 创建保存到 session 里 #防止下面第一次检查账号没有值
    today_str = datetime.date.today().strftime("%Y%m%d")   #获取时间#登陆60*60秒后# 清空session的全部
    errors = {}  # 页面的错误提示
    stmpemail = stmp() #实例化发送邮件的功能
    if request.method =="POST":
        if email != _email: #检查是不是同一个账号，防止验证码用到其他账号
            request.session['email'] = email  # 不是同一个账号，就保存新账号到session里
            request.session['oldTime'] = None  # 同时清空过期时间，重新生成验证码发送邮件
        oldTime = request.session.get('oldTime') # 到session里获取过期的时间
        if oldTime==None or stmpemail.nowtime() > oldTime:  #判断过期的时间
            stmpemail.stmps(request,email)     #发送验证码邮件
            errors['error'] = "验证码邮件已发送成功！60秒后过期！"
        else:
            errors['error'] = "请输入验证码!验证码在%s后过期！" % oldTime

        print('验证码：',request.session['check_smtp'])
        if request.POST.get('check_code'): #前端输入验证码
            if request.session['check_smtp'].upper()  == request.POST.get('check_code').upper():#验证码对比
                username = models.UserProfile.objects.filter(email=email).first()  # 查询数据库有没有这个账号
                print('查询数据库',username)
                if username == None: #数据库没有这个账号就创建
                    models.UserProfile.objects.create(email=email) #数据库创建一个新账号
                user = models.UserProfile.objects.filter(email=email).first()  # 查询数据库有没有这个账号（新账号）
                print('登陆的账号',user.email)
                login(request,user)#记录登录 #Django在数据库创建一条记录 #记住密码，免登录
                request.session['check_smtp'] = None #登陆后验证码进行清空
                request.session['oldTime'] = None   #登陆后过期的时间 进行清空
                request.session.set_expiry(60*60)  #登陆60*60秒后# 清空session的全部
                next_url =request.GET.get('next','/')#跳转的页面,默认为首页
                return redirect(next_url)
            else: #验证码对比不一样
                errors['error']= "验证码错误!"
    return render(request, 'gbacc_ajax/gbacc_fast_login.html', locals())
# ————————44PerfectCRM实现账号快速注册登陆————————

# gbacc_ajax_views.py