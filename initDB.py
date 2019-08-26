import sys, os, datetime
import string, random

pwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pwd)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "PerfectCRM.settings")

import django
django.setup()
print('init DB')

from faker import Faker

from crm import models

faker = Faker('zh-cn')

try:
    for i in range(10):
        u = UserProfile(email=faker.email(), name=faker.name(), password=str(i))
        u.save()
        print(u.name)
except:
    print('already add user')

try:
	roles = ['角色学生','角色销售', '角色老师','角色校长','角色系统维护']
	for role in roles:
	    models.Role.objects.create(name=role)
	branchs = {'北京校区':'北京天安门','广东校区':'广东东莞市','上海校区':'上海黄浦江','福建校区':'福建仙游县','四川校区':'四川成都市'}
	for k, v in branchs.items():
	    models.Branch.objects.create(name=k, addr=v)
	tags = ['好，很好','很有兴趣','兴趣不大','交钱很爽快','随便问问的']
	for tag in tags:
	    models.Tag.objects.create(name=tag)
	models.Course.objects.create(name='Pyton', price='6666', period='40',
	    outline='Python , 是一种面向对象的解释型计算机程序设计语言，具有丰富和强大的库，Python 已经成为继JAVA，C++之后的的第三大语言。 特点：简单易学、免费开源、高层语言、可移植性强、面向对象、可扩展性、可嵌入型、丰富的库、规范的代码等。')
	models.Course.objects.create(name='PHP', price='8888', period='50',
	    outline='PHP语言是目前Web后端开发使用最广泛的语言，几乎绝大多数网站使用。PHP开发快速，开发成本低，周期短，后期维护费用低，开源产品丰富。')
	models.Course.objects.create(name='Java', price='9999', period='60',
	    outline='完成本套餐的学习，学员可以全面掌握后续JavaEE开发所需的Java技术，为后续学习JavaEE开发打下坚实的基础。')
	users = ['ADMIN系统维护','李白销售老师','杜甫销售老师','唐伯虎销售老师','颜真卿老师','罗贯中老师','白居易老师','施耐庵老师','曹雪芹校长']
	for i, user in enumerate(users):
	    models.UserProfile.objects.create(name=user, user_id=i+1)
	class_types = [0,1,2]
	semesters = [int(x)+1 for x in list(string.digits)]
	for semester in semesters:
	    models.ClassList.objects.create(class_type=random.choice([0,1,2]), semester=random.choice(semesters), start_date='2018-03-20', branch_id=1, course_id=1)
except:
    print('already add db')

