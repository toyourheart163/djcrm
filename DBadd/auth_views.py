#随机字符串
import random
import string

from django.shortcuts import render, redirect
# from django.contrib.auth import models
from faker import Faker

from crm import models

fake = Faker('zh-cn')

#添加admin 账号
def auth_user(request):
    if request.method == "GET":
        # user_list = models.User.objects.all()
        user_list = models.UserProfile.objects.all()
        return render(request, 'DBadd/auth_user.html', {'user_list':user_list})
    elif request.method == "POST":
        for i in range(50):
            salt = ''.join(random.sample(string.ascii_letters, 6)) #随机英文
            u=salt
            print(u)
            p='admin123456'
            s='1'
            # models.User.objects.create(username=u,password=p,is_staff=s)
            models.UserProfile.objects.create(name=fake.name(),email=fake.email())
        return  redirect('/DBadd/auth_user/')
