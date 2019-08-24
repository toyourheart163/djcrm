# 随机字符串
import random
from random import choice

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.contrib.auth import models as auth_models
from faker import Faker

from crm import models

faker = Faker('zh-cn')

# 添加"""基本数据"""
def crm_Role(request):
    if request.method == "GET":
        user_list = models.Role.objects.all()
        return render(request, 'DBadd/crm_Role.html', {'user_list': user_list})
    elif request.method == "POST":
        try:
            models.Role.objects.create(name='角色学生')
            models.Role.objects.create(name='角色销售')
            models.Role.objects.create(name='角色老师')
            models.Role.objects.create(name='角色校长')
            models.Role.objects.create(name='角色系统维护')

            models.Branch.objects.create(name='北京校区', addr='北京天安门')
            models.Branch.objects.create(name='广东校区', addr='广东东莞市')
            models.Branch.objects.create(name='上海校区', addr='上海黄浦江')
            models.Branch.objects.create(name='福建校区', addr='福建仙游县')
            models.Branch.objects.create(name='四川校区', addr='四川成都市')

            models.Tag.objects.create(name='好，很好')
            models.Tag.objects.create(name='很有兴趣')
            models.Tag.objects.create(name='兴趣不大')
            models.Tag.objects.create(name='交钱很爽快')
            models.Tag.objects.create(name='随便问问的')

            models.Course.objects.create(name='Pyton', price='6666', period='40',
                                         outline='Python , 是一种面向对象的解释型计算机程序设计语言，具有丰富和强大的库，Python 已经成为继JAVA，C++之后的的第三大语言。 特点：简单易学、免费开源、高层语言、可移植性强、面向对象、可扩展性、可嵌入型、丰富的库、规范的代码等。')
            models.Course.objects.create(name='PHP', price='8888', period='50',
                                         outline='PHP语言是目前Web后端开发使用最广泛的语言，几乎绝大多数网站使用。PHP开发快速，开发成本低，周期短，后期维护费用低，开源产品丰富。')
            models.Course.objects.create(name='Java', price='9999', period='60',
                                         outline='完成本套餐的学习，学员可以全面掌握后续JavaEE开发所需的Java技术，为后续学习JavaEE开发打下坚实的基础。')

            models.UserProfile.objects.create(name='ADMIN系统维护', user_id=1)
            models.UserProfile.objects.create(name='李白销售老师', user_id=2)
            models.UserProfile.objects.create(name='杜甫销售老师', user_id=3)
            models.UserProfile.objects.create(name='唐伯虎销售老师', user_id=4)
            models.UserProfile.objects.create(name='颜真卿老师', user_id=5)
            models.UserProfile.objects.create(name='罗贯中老师', user_id=6)
            models.UserProfile.objects.create(name='白居易老师', user_id=7)
            models.UserProfile.objects.create(name='施耐庵老师', user_id=8)
            models.UserProfile.objects.create(name='曹雪芹校长', user_id=9)

            models.ClassList.objects.create(class_type=1, semester=2, start_date='2018-03-20', branch_id=1, course_id=1)
            models.ClassList.objects.create(class_type=0, semester=5, start_date='2018-03-20', branch_id=1, course_id=1)
            models.ClassList.objects.create(class_type=2, semester=8, start_date='2018-03-20', branch_id=1, course_id=1)
            models.ClassList.objects.create(class_type=0, semester=1, start_date='2018-03-20', branch_id=1, course_id=1)
            models.ClassList.objects.create(class_type=1, semester=3, start_date='2018-03-20', branch_id=1, course_id=1)
            models.ClassList.objects.create(class_type=0, semester=9, start_date='2018-03-20', branch_id=1, course_id=1)
            models.ClassList.objects.create(class_type=2, semester=6, start_date='2018-03-20', branch_id=1, course_id=1)
            models.ClassList.objects.create(class_type=1, semester=20, start_date='2018-03-20', branch_id=1,
                                            course_id=1)
            models.ClassList.objects.create(class_type=0, semester=32, start_date='2018-03-20', branch_id=1,
                                            course_id=1)


        except:
            return HttpResponse('基本数据已经添加了。。。')

        return redirect('/DBadd/crm_Role/')

# 添加"""10账号表"""  #随机学生
def crm_UserProfile(request):
    if request.method == "GET":
        user_list = models.UserProfile.objects.all()
        return render(request, 'DBadd/crm_UserProfile.html', {'user_list': user_list})
    elif request.method == "POST":
        for i in range(50):
            n = faker.name()
            # a = models.UserProfile.objects.values("user_id").all()
            # e = auth_models.User.objects.values("id").all()
            # print('eeeee', e, type(e))
            # x = e.difference(a)
            # for i in x:
            #     print('zzz', x, type(x))

            l = []
            # for i in x:
            #     l.append(i['id'])
            # print('llll', l, type(l))

            # if len(l) == 0:
            if 0:
                return HttpResponse('请添加 admin的用户后，再来添加。。。')
            else:
                # c = choice(l)
                # u = c
                models.UserProfile.objects.create(name=n, email=faker.email())
        return redirect('/DBadd/crm_UserProfile/')


# 添加"""10账号表--11角色表""" #随机学生
def crm_userprofile_roles(request):
    if request.method == "GET":
        user_list = models.UserProfile.objects.all()
        role_list = models.Role.objects.get(id=1)
        return render(request, 'DBadd/crm_userprofile_roles.html', {'user_list': user_list, 'role_list': role_list})
    elif request.method == "POST":
        try:
            for i in range(50):
                b1 = models.Role.objects.get(id=1)
                a = b1.userprofile_set.values("id").all()

                e = models.UserProfile.objects.values("id").all()
                x = e.difference(a)

                l = []
                for i in x:
                    l.append(i['id'])
                print('llll', l, type(l))

                if len(l) == 0:
                    return HttpResponse('请添加 数据 后，再来添加。。。')
                else:
                    c = choice(l)
                    print('c', c, type(c))

                    g1 = models.UserProfile.objects.get(id=c)
                    b1 = models.Role.objects.get(id=1)
                    g1.roles.add(b1)
            return redirect('/DBadd/crm_userprofile_roles/')
        except:
            return HttpResponse('没有数据了。。。')


# 添加"""04客户信息表"""
def crm_Customer(request):
    if request.method == "GET":
        user_list = models.Customer.objects.all()
        return render(request, 'DBadd/crm_Customer.html', {'user_list': user_list})
    elif request.method == "POST":
        for i in range(50):
            Rword = faker.name()
            r=random.randint(5,18)
            Num = "".join(random.choice("0123456789") for i in range(r))  # 随机数字 #保证qq的唯一性
            Cnum = "".join(random.choice("123456789") for i in range(1))  # 随机数字  #不能选择0
            try:
                print(Rword, r, Num, Cnum)
                models.Customer.objects.create(name=Rword, qq=Num, qq_name=Rword, phone=Num, source=1,
                                               referral_from=Rword, consult_courses_id=1, content=Rword,
                                               consultant_id=Cnum, memo=Rword, date='2018-03-21')
            except:
                return HttpResponse('数据重复了。。。')

        return redirect('/DBadd/crm_Customer/')

def crm_ContractTemplate(request):
    if request.method == "GET":
        user_list = models.ContractTemplate.objects.all()
        return render(request, 'DBadd/crm_ContractTemplate.html', {'user_list':user_list})
    elif request.method == "POST":
        try:
            t= '''
            委托方：＿＿{stu_name}＿＿ 
　　法定代表人或负责人：＿＿{stu_name}＿＿ 
　　服务方：＿＿＿＿＿＿＿ 
　　法定代表人或负责人：＿＿＿＿＿＿＿＿＿ 
　　根据《中华人民共和国合同法》的有关规定，经双方当事人协商一致，签订本 
合同。 
　　第一条　项目名称＿＿{course_name}＿＿。 
　　（注：本参考格式适用于下列技术服务活动：进行设计、工艺、制造、试验以 
及农作物育种，畜禽的饲养等方面的技术指导、讲解技术资料、解决和解答技术问 
题；进行示范操作；传授计算机软件的编制技术、先进仪器设备的装配，使用技术 
等等。） 
　　第二条　培训的内容和要求：＿＿＿＿＿＿＿。 
　　第三条　培训计划、进度、期限：＿＿＿＿＿＿＿。 
　　第四条　培训地点和方式：＿＿＿＿＿＿＿＿＿＿＿＿。 
　　第五条　服务方（教师）的资历和水平：＿＿＿＿＿＿＿＿。 
　　第六条　学员的人数和质量：＿＿＿＿＿＿＿＿＿＿＿。 
　　第七条　教员、学员的食宿、交通、医疗费用的支付和安排＿＿＿＿。 
　　第八条　报酬及其支付方式：＿＿＿＿＿＿＿＿＿＿。 
　　第九条　委托方的违约责任：＿＿＿＿＿＿＿＿＿。 
　　１．委托方未按合同提供培训条件，影响合同履行的，约定的报酬仍应如数支 
付； 
　　２．擅自将服务方要求保密的技术资料引用、发表和提供给第三方，应支付数 
额为＿＿＿＿的违约金； 
　　第十条　服务方的违约责任： 
　　１．服务方未按合同制订培训计划，影响培训工作质量的，应当减收＿＿＿％ 
的报酬； 
　　２．服务方提供的师资不符合合同要求，服务方有义务予以重新配备；未按合 
同规定完成培训工作的，应免收报酬。 
　　第十一条　保密条款：＿＿＿＿＿＿＿＿ 
　　当事人双方应对下列技术资料承担保密义务：＿＿＿＿＿＿。 
　　第十二条　有关技术成果归属条款 
　　在履行合同过程中，服务方利用委托方提供的技术资料和工作条件所完成的新 
的技术成果，属于服务方；委托方利用服务方的工作成果所完成的新技术成果，属 
于委托方。对新的技术成果享有就该技术成果取得的精神权利（如获得奖金、奖章、 
荣誉证书的权利）、经济权利（如专利权、非专利技术的转让权，使用权等）和 
其它利益。 
　　第十三条　本合同争议的解决办法：＿＿＿＿＿＿。 
　　本合同自双方当事人签字、盖章后生效。
委托方负责人（或授权代表）　　　　　　服务方负责人（或授权代表） 
　　签字：＿＿{stu_name}＿＿（盖章）　　　　　签名：＿＿＿＿（盖章） 
　　签字时间：＿＿＿＿＿＿＿＿＿　　　　　签字时间：＿＿＿＿＿＿＿＿＿ 
　　签字地点：＿＿＿＿＿＿＿＿＿　　　　　签字地点：＿＿＿＿＿＿＿＿＿ 
　　开户银行：＿＿＿＿＿＿＿＿＿　　　　　开户银行：＿＿＿＿＿＿＿＿＿ 
　　帐号：＿＿＿＿＿＿＿＿＿＿＿　　　　　帐号：＿＿＿＿＿＿＿＿＿＿＿ 
　　委托方担保人（名称）：＿＿＿　　　　　服务方担保人（名称）：＿＿＿ 
　　地址：＿＿＿＿＿＿＿＿＿＿＿　　　　　地址：＿＿＿＿＿＿＿＿＿＿＿ 
　　负责人（或授权代表）　　　　　　　　　负责人（或授权代表） 
　　签字：＿＿＿＿＿＿＿＿（盖章）　　　　签字：＿＿＿＿＿＿＿＿（盖章） 
　　签字时间：＿＿＿＿＿＿＿＿＿　　　　　签字时间：＿＿＿＿＿＿＿＿＿ 
　　签字地点：＿＿＿＿＿＿＿＿＿　　　　　签字地点：＿＿＿＿＿＿＿＿＿ 
　　开户银行：＿＿＿＿＿＿＿＿＿　　　　　开户银行：＿＿＿＿＿＿＿＿＿ 
　　帐号：＿＿＿＿＿＿＿＿＿＿＿　　　　　帐号：＿＿＿＿＿＿＿＿＿＿＿'''

            models.ContractTemplate.objects.create(name='技术合同：专业技术培训协议',template=t)
        except:
            return HttpResponse('数据错误！重复了吧。。。')

        return  redirect('/DBadd/crm_ContractTemplate/')

def DBadd(request):
    return  render(request,'DBadd/DBadd.html',locals())

def crm_CourseRecord(request):
    if request.method == "GET":
        user_list = models.CourseRecord.objects.all()
        return render(request, 'DBadd/crm_CourseRecord.html', {'user_list': user_list})
    elif request.method == "POST":
        a=1
        for i in range(2):
            try:
                # 创建班级  节课
                models.CourseRecord.objects.create(from_class_id=1, day_num=a, teacher_id=1, has_homework=1, outline=1,date='2018-05-05')
                models.CourseRecord.objects.create(from_class_id=2, day_num=a, teacher_id=1, has_homework=1, outline=1,date='2018-05-05')
                models.CourseRecord.objects.create(from_class_id=3, day_num=a, teacher_id=1, has_homework=1, outline=1,date='2018-05-05')
                a+=1
            except:
                return HttpResponse('数据错误！重复了吧。。。')
        return redirect('/DBadd/crm_CourseRecord/')

def crm_Enrollment(request):
    if request.method == "GET":
        user_list = models.Enrollment.objects.all()
        return render(request, 'DBadd/crm_Enrollment.html', {'user_list': user_list})
    elif request.method == "POST":
        a=1
        for i in range(6):
            try:
                # 创建报名信息
                models.Enrollment.objects.create(customer_id=a, enrolled_class_id=1, consultant_id=1, contract_review=1,contract_agreed=1,contract_approved=1,Pay_cost=1,date='2018-05-05 14:45:19.537109')
                models.Enrollment.objects.create(customer_id=a, enrolled_class_id=2, consultant_id=1, contract_review=1,contract_agreed=1,contract_approved=1,Pay_cost=1,date='2018-05-05 14:45:19.537109')
                models.Enrollment.objects.create(customer_id=a, enrolled_class_id=3, consultant_id=1, contract_review=1,contract_agreed=1,contract_approved=1,Pay_cost=1,date='2018-05-05 14:45:19.537109')
                a+=1
                # 创建报名信息
            except:
                return HttpResponse('数据错误！重复了吧。。。')
        return redirect('/DBadd/crm_Enrollment/')
