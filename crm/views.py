import random
import os
import json
import datetime  # 获取时间#登陆过期
import string

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError  #主动捕捉错误信息
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import StreamingHttpResponse #页面返回

# send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)

from crm import models, forms
from PerfectCRM import settings

# 发送邮件的功能 #验证码#密码
class stmp():
    def __init__(self):
        self.emaillist = []  # 发送给谁
        self.code = None  # 验证码#密码

    def stmps(self, request, email, msg_mail):  # 传参数#页面，session #邮箱，发送给谁 #内容
        self.emaillist.append(email)  # 将邮箱地址添加到调用Django发送邮件功能
        # ——————生成验证码——————
        _letter_cases = "abcdefghjkmnpqrstuvwxy"  # 小写字母，去除可能干扰的i，l，o，z
        _upper_cases = _letter_cases.upper()  # 大写字母
        _numbers = ''.join(map(str, range(3, 10)))  # 数字
        chars = ''.join((_letter_cases, _upper_cases, _numbers))  # 变成一条字符串
        list = random.sample(chars, 4)  # 从一条字符串随机选4个字符变成列表
        self.code = ''.join(list)  # 列表变字符串
        # ——————生成验证码——————
        # ——————调用Django发送邮件——————
        title = 'PerfectCRM项目自动邮件：%s' % self.code  # 邮件标题#防止一样的内容被邮箱屏蔽
        send_mail(title,  # 邮件标题
                  msg_mail,  # 验证码内容
                  'perfectcrm@sina.cn',  # 发送的邮箱  #根据情况重新配置
                  self.emaillist,  # 接受的邮箱
                  fail_silently=False,  # 静默,抛出异常
                  )
        print('发送邮件成功！没收到要换标题！检查发送邮箱的配置！')

# 报名填写 销售
@login_required  # 登陆后页面才能访问
def enrollment(request, customer_id):
    msgs = {}  # 错误信息
    customer_obj = models.Customer.objects.get(id=customer_id)  # 取到客户信息记录 #返回到页面#报名人
    consultant_obj = models.UserProfile.objects.get(id=request.user.id)  # 报名课程顾问

    stmp_mail = {}  # 邮件发送成功
    stmpemail = stmp()  # 实例化发送邮件的功能
    email = request.POST.get('email')  # 让页面POST提交的值，在页面GET后仍然存在显示
    if request.method == "POST":
        enroll_form = forms.EnrollmentForm(request.POST)  # 获取数据
        if enroll_form.is_valid():  # 表单验证

            # ————————50PerfectCRM实现CRM客户报名流程学生合同URL随机码————————
            msg = "http://127.0.0.1:8000/crm/customer/registration/{enroll_obj_id}/{random_str}/ "
            random_str = ''.join(random.sample(string.ascii_lowercase + string.digits, 8))  # 生成8位随机字符串 #URL使用
            url_str = '''customer/registration/{enroll_obj_id}/{random_str}/'''  # 报名链接
            # ————————50PerfectCRM实现CRM客户报名流程学生合同URL随机码————————

            try:
                enroll_form.cleaned_data['customer'] = customer_obj  # 添加学员对象 记录 #报名人
                enroll_form.cleaned_data['consultant'] = consultant_obj  # 报名课程顾问
                enroll_obj = models.Enrollment.objects.create(**enroll_form.cleaned_data)  # 创建记录

                # ————————50PerfectCRM实现CRM客户报名流程学生合同URL随机码————————
                # msgs['msg']=msg.format(enroll_obj_id=enroll_obj.id)#报名记录对应的id,随机字符串，报名链接
                sort_url = enroll_obj.id  # 获取报名表对应的ID
                cache.set(enroll_obj.id, random_str, 61000)  # 加入过期时间   #URL使用    # cache缓存
                msgs['msg'] = msg.format(enroll_obj_id=enroll_obj.id, random_str=random_str)  # 报名记录对应的id,随机字符串，报名链接
                url_str = url_str.format(enroll_obj_id=enroll_obj.id, random_str=random_str)  # 报名链接
                print(url_str)
                # ————————50PerfectCRM实现CRM客户报名流程学生合同URL随机码————————
            except IntegrityError as e:
                # 取到这条记录
                enroll_obj = models.Enrollment.objects.get(customer_id=customer_obj.id,
                                                           enrolled_class_id=enroll_form.cleaned_data[
                                                               'enrolled_class'].id)

                if enroll_obj.contract_agreed:#学员已经同意合同，提交了身份证
                    #return redirect('/crm/contract_review/%s/'%enroll_obj.id)#跳转到审核页面
                    return render(request,'crm/contract_prompt.html',locals())#跳转提示页面
                enroll_form.add_error('__all__', '记录已经存在，不能重复创建！')

                # ————————50PerfectCRM实现CRM客户报名流程学生合同URL随机码————————
                # msgs['msg']=msg.format(enroll_obj_id=enroll_obj.id)#报名记录对应的id
                cache.set(enroll_obj.id, random_str, 61000)  # 加入过期时间  #URL使用    # cache缓存
                msgs['msg'] = msg.format(enroll_obj_id=enroll_obj.id, random_str=random_str)  # 报名记录对应的id
                url_str = url_str.format(enroll_obj_id=enroll_obj.id, random_str=random_str)  # 报名链接
                # ————————50PerfectCRM实现CRM客户报名流程学生合同URL随机码————————

            if email:
                # ————————50PerfectCRM实现CRM客户报名流程学生合同URL随机码————————
                # msg_mail = "http://127.0.0.1:8000/crm/customer/registration/%s" %enroll_obj.id
                msg_mail = "http://127.0.0.1:8000/crm/customer/registration/%s/%s" %(enroll_obj.id,random_str)
                # ————————50PerfectCRM实现CRM客户报名流程学生合同URL随机码————————
                stmpemail.stmps(request, email, msg_mail)  # 发送邮件
                stmp_mail['ok'] = "邮件已发送成功！"

    else:
        enroll_form = forms.EnrollmentForm()  # modelform表单
    return render(request, 'crm/enrollment.html', locals())
# ————————47PerfectCRM实现CRM客户报名流程————————

# ————————50PerfectCRM实现CRM客户报名流程学生合同URL随机码————————
from django.shortcuts import HttpResponse #页面返回
# def stu_registration(request,enroll_id):
def stu_registration(request,enroll_id,random_str):
    # enroll_obj=models.Enrollment.objects.get(id=enroll_id)#获取报名记录
    if cache.get(enroll_id) == random_str:  # 判断链接失效了没有
        enroll_obj = models.Enrollment.objects.get(id=enroll_id)  # 报名记录
# ————————50PerfectCRM实现CRM客户报名流程学生合同URL随机码————————

        # ————————51PerfectCRM实现CRM客户报名流程学生合同上传照片————————
        enrolled_path='%s/%s/'%(settings.ENROLLED_DATA,enroll_id)#证件上传路径
        img_file_len=0  #文件
        if os.path.exists(enrolled_path):#判断目录是否存在
            img_file_list=os.listdir(enrolled_path)#取目录 下的文件
            img_file_len=len(img_file_list)
        # ————————51PerfectCRM实现CRM客户报名流程学生合同上传照片————————

    # ————————49PerfectCRM实现CRM客户报名流程学生合同表单验证————————
        # ————————50PerfectCRM实现CRM客户报名流程学生合同URL随机码————————
        if request.method == "POST":

            # ————————51PerfectCRM实现CRM客户报名流程学生合同上传照片————————
            ret=False
            data=request.POST.get('data')
            if data:#如果有删除动作
                del_img_path="%s/%s/%s"%(settings.ENROLLED_DATA,enroll_id,data)#路径
                print(del_img_path,'=-=-=-=-=-=')
                os.remove(del_img_path)
                ret=True
                return HttpResponse(json.dumps(ret))
            if request.is_ajax():#ajax上传图片 #异步提交
                print('ajax上传图片 #异步提交中。。。 ',request.FILES)
                enroll_data_dir="%s/%s"%(settings.ENROLLED_DATA,enroll_id)#路径  #重要信息不能放在静态文件中
                if not os.path.exists(enroll_data_dir):#如果不存目录
                    os.makedirs(enroll_data_dir,exist_ok=True)#创建目录
                for k,file_obj in request.FILES.items():   #循环字典 #上传的文件
                    with open("%s/%s"%(enroll_data_dir,file_obj.name),'wb') as f: #打开一个文件#路径#获取文件名
                        for chunk in file_obj.chunks():#循环写入文件 # chunks块
                            f.write(chunk)  #保存文件
                return HttpResponse('上传完成！')
            # ————————51PerfectCRM实现CRM客户报名流程学生合同上传照片————————

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
    # customer_form = forms.CustomerForm(instance=enroll_obj.customer)  # 生成表单
    # ————————49PerfectCRM实现CRM客户报名流程学生合同表单验证————————

        return render(request,'crm/stu_registration.html',locals())
        # ————————50PerfectCRM实现CRM客户报名流程学生合同URL随机码————————
# ————————48PerfectCRM实现CRM客户报名流程学生合同————————
    # ————————50PerfectCRM实现CRM客户报名流程学生合同URL随机码————————
    else:
        return HttpResponse('链接失效，非法链接，请自重！')
    # ————————50PerfectCRM实现CRM客户报名流程学生合同URL随机码————————

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
    # customer_form = forms.CustomerForm(instance=enroll_obj.customer)  # 生成表单
    # ————————49PerfectCRM实现CRM客户报名流程学生合同表单验证————————

    return render(request,'crm/stu_registration.html',locals())

from django.shortcuts import redirect
#查询流程提示页面

def contract_prompt(request,enroll_id):
    enroll_obj=models.Enrollment.objects.get(id=enroll_id)#取对象
    enroll_form= forms.EnrollmentForm(instance=enroll_obj)#报名表对象
    customers_form= forms.CustomerForm(instance=enroll_obj.customer)#学员的信息
    return render(request,'crm/contract_prompt.html',locals())
# #待审核
def not_audit(request):
    sign=models.Enrollment.objects.all()#所有的报名表
    print(sign,'sign----->')
    return render(request, 'crm/not_audit.html', locals())#

#审核合同
@login_required # 登陆后页面才能访问
def contract_review(request,enroll_id):
    enroll_obj=models.Enrollment.objects.get(id=enroll_id)#取对象
    contract_review = request.user.name #当前登陆人 #合同审核人
    #payment_form=forms.PaymentForm()#生成表单
    enroll_form= forms.EnrollmentForm(instance=enroll_obj)#报名表对象
    customer_form= forms.CustomerForm(instance=enroll_obj.customer)#学员的信息
    enrolled_path='%s/%s/'%(settings.ENROLLED_DATA,enroll_id)#证件上传路径
    if os.path.exists(enrolled_path):#判断目录是否存在
        file_list=os.listdir(enrolled_path)#取目录 下的文件
        imgs_one=file_list[0]  #图片1
        imgs_two=file_list[1]  #图片2
    if request.method=="POST":
        enroll_obj.contract_approved = True  # 审核通过
        enroll_obj.save() #保存
        enroll = models.Enrollment.objects.filter(id=enroll_id).update(contract_review=contract_review)#合同审核人
        print('审核通过。。。')
        return redirect('/crm/not_audit/')#跳转到待审核
    return render(request, 'crm/contract_review.html', locals())#
#驳回合同
def enrollment_rejection(request,enroll_id):
    enroll_obj=models.Enrollment.objects.get(id=enroll_id)#报名表的对象
    enroll_obj.contract_agreed=False#修改学员已经同意核同
    enroll_obj.save() #保存
    return redirect('/crm/customer/%s/enrollment/'%enroll_obj.customer.id)#跳转到enrollment_rejection

# #待缴费
def not_payment(request):
    sign=models.Enrollment.objects.all()#所有的报名表
    return render(request, 'crm/not_payment.html', locals())#

# 已缴费
def already_payment(request):
    sign=models.Enrollment.objects.all()#所有的报名表
    return render(request, 'crm/already_payment.html', locals())#

#缴费视图
@login_required # 登陆后页面才能访问
def payment(request,enroll_id):
    sign=models.Payment.objects.all()#所有的报名表#前端对比用户#缴费记录
    enroll_obj=models.Enrollment.objects.get(id=enroll_id)#取对象
    errors={}  #错误信息
    if request.method=="POST":
        payment_amount=request.POST.get('amount')#缴费金额
        consultant = models.UserProfile.objects.get(id=request.user.id)  #财务人员 #当前登陆人
        if payment_amount:
            payment_amount=int(payment_amount)  #转数字类型
            if payment_amount<500:
                errors['err']='缴费金额不得低于500元！'
            else: #生成forms
                payment_obj=models.Payment.objects.create(
                    customer=enroll_obj.customer,##客户表 学员
                    course=enroll_obj.enrolled_class.course,#所报课程
                    consultant=consultant,# 财务人员
                    amount=payment_amount,#缴费金额
                )
                enroll_obj.Pay_cost=True#已缴费
                enroll_obj.save()   #保存
                enroll_obj.customer.status=0#修改报名状态 为已报名#根据数据库
                enroll_obj.customer.save()  #保存
                return redirect('/crm/not_payment')#客户表
        else:
            errors['err']='金额不能为空！'
    else:
        payment_form= forms.PaymentForm()#生成表单
    return render(request, 'crm/payment.html', locals())

@login_required
def student_course(request):
    if request.user.stu_account:
        enrollmentlist=request.user.stu_account.enrollment_set.all()#根据账号表关联的ID获取06学员报名信息表
    return  render(request, 'crm/student_course.html', locals())

#学生上课记录列表
@login_required # 登陆后页面才能访问
def studyrecords(request,enroll_obj_id):
    enroll_obj=models.Enrollment.objects.get(id=enroll_obj_id)#根据ID获取06学员报名信息表
    studyrecordlist=enroll_obj.studyrecord_set.all()#根据06学员报名信息表的ID获取09学习纪录
    return render(request,'crm/studyrecords.html',locals())

@login_required#登陆才能访问
def homework_detail(request,enroll_obj_id,studyrecord_id):
    studyrecord_obj=models.StudyRecord.objects.get(id=studyrecord_id)#取学习记录 对象
    enroll_obj=models.Enrollment.objects.get(id=enroll_obj_id)#取班级对象

    #               作业根目录    班级ID      上课记录ID               学习记录ID
    homework_path="{base_dir}/{class_id}/{course_record_id}/{studyercord_id}/".format(
        base_dir=settings.HOMEWORK_DATA, #静态配置文件
        class_id=studyrecord_obj.student.enrolled_class_id,#09学习纪录#学生名字#所报班级ID号
        course_record_id=studyrecord_obj.course_record_id,#09学习纪录#每节课上课纪录表
        studyercord_id=studyrecord_obj.id##09学习纪录
    )
    print('homework_path路径：',studyrecord_obj.student.enrolled_class_id,studyrecord_obj.course_record_id,studyrecord_obj.id)

    if os.path.exists(homework_path):#判断目录是否存在
        file_lists = []  # 已经上传的文件列表
        for file_name in os.listdir( homework_path ):
            f_path = '%s/%s' % (homework_path, file_name)  # 文件名字
            modify_time = time.strftime( "%Y-%m-%d %H:%M:%S", time.gmtime( os.stat( f_path ).st_mtime ) )  # 文件上传时间
            file_lists.append( [file_name, os.stat( f_path ).st_size, modify_time] )  # 添加到文件列表#文件名字#文件大小文件上传时间


    if request.method=="POST":#上传
        ret=False
        data=request.POST.get('data') #ajax
        if data:#如果有删除动作
            del_f_path="%s/%s"%(homework_path,data)#文件路径
            print('删除文件,路径:',del_f_path)
            os.remove(del_f_path) #删除
            ret=True
            return HttpResponse(json.dumps(ret))#ret=False
        if request.is_ajax():  # ajax上传图片 #异步提交
            print("POST",request.POST)
            if not os.path.isdir( homework_path ):  # 没有目录 #isdir返回true,如果路径名是指现有的目录。
                os.makedirs( homework_path, exist_ok=True )  # 创建目录　　
            for k,v in request.FILES.items():#上传的文件
                with open('%s/%s'%(homework_path,v.name),'wb') as f:#chunk 写入文件
                    for chunk in v.chunks(): #循环写文件
                        f.write(chunk)
            return HttpResponse( json.dumps( {"status": 0, 'mag': "上传完成！", 'file_lists': file_lists} ) )  # 上传文件返回

    if request.method=="POST":#上传
        link = request.POST.get( 'link' )  # 让页面POST提交的值，在页面GET后仍然存在显示
        if link:
            homework_link=models.StudyRecord.objects.filter( id=studyrecord_id ).update(homework_link=link)
            return redirect('/crm/homework_detail/%s/%s/' %(enroll_obj_id,studyrecord_id) )#跳转到enrollment_rejection
    return render(request,'crm/homework_detail.html',locals())


#讲师班级
@login_required
def teacher_class(request):
    # user_id=request.user.id #当前登陆的ID
    # classlist=models.UserProfile.objects.get(id=user_id).classlist_set.all()#讲师所教班级
    classes_obj=request.user.classlist_set.all() #根据 登陆的ID 获取02班级表
    return render(request,'crm/teacher_class.html',locals())

# 讲师班级课节详情
@login_required
def teacher_class_detail(request,class_id):
    # classes_obj=models.UserProfile.objects.get(id=user_id).classlist_set.get(id=class_id)#所选的班级
    classes_obj=request.user.classlist_set.get(id=class_id) #根据 登陆的ID 获取02班级表
    courserecordlist=classes_obj.courserecord_set.all()#根据 02班级表的ID 获取09学习纪录
    return render(request, 'crm/teacher_classes_detail.html', locals())

# 讲师班级
@login_required  # 登陆后页面才能访问
def teacher_class(request):
    # user_id=request.user.id #当前登陆的ID
    # classlist=models.UserProfile.objects.get(id=user_id).classlist_set.all()#讲师所教班级
    classes_obj = request.user.classlist_set.all()  # 根据 登陆的ID 获取02班级表
    return render( request, 'bpm_teacher/teacher_class.html', locals() )

# 讲师班级课节详情
@login_required  # 登陆后页面才能访问
def teacher_class_detail(request, class_id):
    # user_id=request.user.id #当前登陆的ID
    # classes_obj=models.UserProfile.objects.get(id=user_id).classlist_set.get(id=class_id)#所选的班级
    classes_obj = request.user.classlist_set.get( id=class_id )  # 根据 登陆的ID 获取02班级表
    courserecordlist = classes_obj.courserecord_set.all()  # 根据 02班级表的ID 获取09学习纪录
    return render( request, 'bpm_teacher/teacher_classes_detail.html', locals() )
# ————————62PerfectCRM实现CRM讲师讲课记录————————

# ————————63PerfectCRM实现CRM讲师下载作业————————
# 本节课的学员
@login_required  # 登陆后页面才能访问
def teacher_lesson_detail(request, class_id, courserecord_id):
    # classes_obj=models.UserProfile.objects.get(id=request.user.id).classlist_set.get(id=class_id)#所选的班级
    classes_obj = request.user.classlist_set.get( id=class_id ) # 根据 登陆的ID 获取02班级表
    courserecordlist = classes_obj.courserecord_set.get( id=courserecord_id )  # 根据 前端的ID 获取08每节课上课纪录表

    # studyrecord_list=models.CourseRecord.objects.get(id=courserecord_id).studyrecord_set.all()#取本节课所有学员
    studyrecord_list = courserecordlist.studyrecord_set.all()  # 根据08每节课上课纪录表 #获取09学习纪录 #取本节课所有学员

    for i in studyrecord_list:  # 循环本节课所有学员 交作业的状态
        studyrecord_id = i.id  # 获取本节课所有学员的ID
        if studyrecord_id:  # 有获取到ID
            HOMEWORK_path = '%s/%s/%s/%s/' % (settings.HOMEWORK_DATA, class_id, courserecord_id, studyrecord_id)  # 作业目录
            if os.path.exists( HOMEWORK_path ):  # 判断目录是否存在
                try:#防止后台误删文件
                    file_list = os.listdir( HOMEWORK_path )  # 取目录 下的文件
                    isfile = os.path.isfile( '%s%s' % (HOMEWORK_path, file_list[0]) )  # 判断是不是文件
                    studyrecord_list.filter( id=studyrecord_id ).update( delivery=isfile )  # 更新交付作业状态
                except:
                    studyrecord_list.filter( id=studyrecord_id ).update( delivery=False )  # file_list 出错# 更新交付作业状态
            else:
                studyrecord_list.filter( id=studyrecord_id ).update( delivery=False )# 更新交付作业状态
    return render( request, 'bpm_teacher/teacher_lesson_detail.html', locals() )

# 学员作业下载
@login_required  # 登陆后页面才能访问
def howk_down(request, class_id, courserecord_id, studyrecord_id):
    HOMEWORK_path = '%s/%s/%s/%s/' % (settings.HOMEWORK_DATA, class_id, courserecord_id, studyrecord_id)  # 作业目录
    print( '下载作业目录:', HOMEWORK_path )

    def file_iterator(file_path, chunk_size=512):  # 获取文件 #chunk_size每次读取的大小 #文件迭代器
        with open( file_path, 'rb', ) as f:  # 循环打开 文件#以二进制读模式打开
            while True:  # 如果有文件
                byte = f.read( chunk_size )  # read读最多大小字节,作为字节返回。#获取文件大小
                if byte:
                    yield byte  # 返回 yield 后的值作为第一次迭代的返回值. 循环下一次，再返回，直到没有可以返回的。
                else:
                    break  # 没有字节就中止

    if os.path.exists( HOMEWORK_path ):  # 判断目录是否存在
        try:#防止后台误删文件
            file_list = os.listdir( HOMEWORK_path )  # 取目录 下的文件
            print( '文件名：', file_list, type( file_list ) )
            file_path = '%s%s' % (HOMEWORK_path, file_list[0])  # 下载文件路径
            print( '下载文件路径：', file_path )
            response = StreamingHttpResponse( file_iterator( file_path ) )  # StreamingHttpResponse是将文件内容进行流式传输
            response['Content-Type'] = 'application/octet-stream'  # 文件类型 #应用程序/octet-stream.*（ 二进制流，不知道下载文件类型）
            file_name = 'attachment;filename=%s' % file_list[0]  # 文件名字# 支持中文
            response['Content-Disposition'] = file_name.encode()  # 支持中文#编码默认encoding='utf-8'
            return response  # 返回下载 请求的内容
        except:
            models.StudyRecord.objects.get( id=studyrecord_id ).update( delivery=False )  # 更新交付作业状态 # file_list 出错
    return redirect( '/bpm/teacher_lesson_detail/%s/%s/' % (class_id, courserecord_id) )  # 返回##本节课的学员