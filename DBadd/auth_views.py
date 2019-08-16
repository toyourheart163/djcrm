from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth import models

#随机字符串
import random
import string


#添加admin 账号
def auth_user(request):
    if request.method == "GET":
        user_list = models.User.objects.all()
        return render(request, 'DBadd/auth_user.html', {'user_list':user_list})
    elif request.method == "POST":
        for i in range(50):
            salt = ''.join(random.sample(string.ascii_letters, 6)) #随机英文
            u=salt
            print(u)
            p='admin123456'
            s='1'
            models.User.objects.create(username=u,password=p,is_staff=s)
        return  redirect('/DBadd/auth_user/')
