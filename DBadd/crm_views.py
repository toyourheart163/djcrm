from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse

from crm import models
from django.contrib.auth import models as auth_models

# 随机字符串
import random
from random import choice


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

            Rword = ''.join(''.join([chr(random.randint(0x4E00, 0x9FBF)) for i in range(3)]).split())  # 随机中文
            n = Rword

            a = models.UserProfile.objects.values("user_id").all()
            e = auth_models.User.objects.values("id").all()
            print('eeeee', e, type(e))
            x = e.difference(a)
            # for i in x:
            #     print('zzz', x, type(x))

            l = []
            for i in x:
                l.append(i['id'])
            print('llll', l, type(l))

            if len(l) == 0:
                return HttpResponse('请添加 admin的用户后，再来添加。。。')
            else:
                c = choice(l)
                u = c
                models.UserProfile.objects.create(name=n, user_id=u)
        return redirect('/DBadd/crm_UserProfile/')


# 添加"""10账号表--11角色表""" #随机学生
def crm_userprofile_roles(request):
    if request.method == "GET":
        user_list = models.UserProfile.objects.all()
        role_list = models.Role.objects.get(id=1)
        return render(request, 'crm_userprofile_roles.html', {'user_list': user_list, 'role_list': role_list})
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
            Rword = ''.join(''.join([chr(random.randint(0x4E00, 0x9FBF)) for i in range(3)]).split())  # 随机中文
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
