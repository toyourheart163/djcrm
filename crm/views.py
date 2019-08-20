from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError  #主动捕捉错误信息

from crm import models, forms

from django.core.mail import send_mail
# send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
import random
import datetime  # 获取时间#登陆过期

# Create your views here.
@login_required # 登陆后页面才能访问
def enrollment(request,customer_id):
    msgs={} #错误信息
    customer_obj=models.Customer.objects.get(id=customer_id)#取到客户信息记录 #返回到页面#报名人
    consultant_obj=models.UserProfile.objects.get(id=request.user.id)#报名课程顾问

    stmp_mail = {}  #邮件发送成功
    stmpemail = stmp() #实例化发送邮件的功能
    email = request.POST.get('email')  # 让页面POST提交的值，在页面GET后仍然存在显示
    if request.method=="POST":
        enroll_form= forms.EnrollmentForm(request.POST)#获取数据
        if enroll_form.is_valid():#表单验证
            msg = "/crm/customer/registration/{enroll_obj_id}/"
            try:
                enroll_form.cleaned_data['customer']=customer_obj#添加学员对象 记录 #报名人
                enroll_form.cleaned_data['consultant'] = consultant_obj#报名课程顾问
                enroll_obj = models.Enrollment.objects.create(**enroll_form.cleaned_data)#创建记录
                msgs['msg'] = msg.format(enroll_obj_id=enroll_obj.id)#报名记录对应的id
            except IntegrityError as e:
                #取到这条记录
                enroll_obj = models.Enrollment.objects.get(customer_id=customer_obj.id,
                                                         enrolled_class_id=enroll_form.cleaned_data['enrolled_class'].id)
                enroll_form.add_error('__all__','记录已经存在，不能重复创建！')
                msgs['msg'] = msg.format(enroll_obj_id=enroll_obj.id)#报名记录对应的id
            if email:
                msg_mail = "/crm/customer/registration/%s/"%enroll_obj.id
                stmpemail.stmps(request, email,msg_mail)  # 发送邮件
                stmp_mail['ok'] = "邮件已发送成功！"

    else:
        enroll_form= forms.EnrollmentForm()#modelform表单
    return render(request, 'crm/enrollment.html', locals())
# ————————47PerfectCRM实现CRM客户报名流程————————


# ————————48PerfectCRM实现CRM客户报名流程学生合同————————
#学员合同签定
def stu_registration(request,enroll_id):
    enroll_obj = models.Enrollment.objects.get(id=enroll_id)#获取报名记录
    if request.method == "POST":
        customer_form = forms.CustomerForm(request.POST, instance=enroll_obj.customer)  # 生成表单验证
        if customer_form.is_valid():  # 表单验证通过
            customer_form.save()  # 保存
            enroll_obj.contract_agreed = True  # 同意协议
            enroll_obj.save()  # 保存
            status = 1  # 修改报名状态 # 1 已经报名
            return render(request, 'crm/stu_registration.html', locals())

    else:
        if enroll_obj.contract_agreed == True:  # 如果协议已经签订
            status = 1  # 修改报名状态 # 1 已经报名
        else:
            status = 0
        customer_form = forms.CustomerForm(instance=enroll_obj.customer)  # 生成表单
    # customer_form = bpm_forms.CustomerForm(instance=enroll_obj.customer)  # 生成表单
    # ————————49PerfectCRM实现CRM客户报名流程学生合同表单验证————————

    return render(request,'crm/stu_registration.html',locals())