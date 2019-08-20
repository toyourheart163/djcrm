# account.py
# ————————40PerfectCRM实现全局账号注册+验证码+页面刷新保留信息————————
from .base import BaseForm  #重写
from django.core.exceptions import ValidationError #错误信息
from django import forms as django_forms           # forms
from django.forms import fields as django_fields     #字段
from crm import models #数据库


#注册验证
class RegisterForm(BaseForm, django_forms.Form):
    name=django_fields.CharField(
        min_length=3,
        max_length=20,
        error_messages={'required': '用户名不能为空.',  #默认输入这个
                        'min_length': "用户名长度不能小于3个字符",
                        'max_length': "用户名长度不能大于32个字符"},     )
    email=django_fields.EmailField(
        error_messages={'required': '邮箱不能为空.','invalid':"邮箱格式错误"}, )
    password = django_fields.RegexField(
        #正则表达  配置密码复杂度
        # '^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
        '',
        min_length=6,
        max_length=32,
        error_messages={'required': '密码不能为空.',  #默认输入这个
                        'invalid': '密码必须包含数字，字母、特殊字符', # 正则表达
                        'min_length': "密码长度不能小于6个字符",
                        'max_length': "密码长度不能大于32个字符",
                        'message':None},        )
    confirm_password=django_fields.CharField(
        error_messages={'required': '确认密码不能为空.',
                        'invalid': '确认密码不对', },  )
    check_code = django_fields.CharField(
        error_messages={'required': '验证码不能为空.'},     )

    #内置勾子
    #用户名重复查询
    def clean_username(self):
        #查询是否存在
        name=self.cleaned_data['name']  #cleaned_data 就是读取表单返回的值，返回类型为字典dict型
        u =models.UserProfile.objects.filter(name=name).count()  #查询数据库
        if not u:
            return self.cleaned_data['name']
        else:
            raise ValidationError(message='用户名已经存在',code='invalid')
    #邮箱重复查询
    def clean_email(self):
        email=self.cleaned_data['email']
        e=models.UserProfile.objects.filter(email=email).count() #查询数据库
        if not e:
            return  self.cleaned_data['email']
        else:
            raise ValidationError('邮箱已经被注册!',code='invalid')

    #确认密码
    def clean_confirm_password(self):
        pwd1=self.request.POST.get('password')  #通过POST 获取前端 输入的值
        pwd2=self.cleaned_data['confirm_password'] #name="confirm_password"
        if pwd1 != pwd2:
            raise ValidationError('二次输入密码不匹配')
        else:
            return self.cleaned_data['confirm_password']

    # 验证码 校对
    def clean_check_code(self):
            #调用check_code.py # 获取生成的验证码                  #获取输入的验证码
        if self.request.session.get('CheckCode').upper() != self.request.POST.get('check_code').upper():
            raise ValidationError(message='验证码错误', code='invalid')
        else:
            return self.cleaned_data['check_code']
# ————————40PerfectCRM实现全局账号注册+验证码+页面刷新保留信息————————

# account.py