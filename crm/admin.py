from django.contrib import admin
from django.shortcuts import render

# Register your models here.
from crm import models #从crm导入models

from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from crm.models import UserProfile


#重写admin
class UserCreationForm(forms.ModelForm):
    """　　
    一个表单来创建新用户。包括所有必需的字段,加上重复密码。
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('email', 'name')

    def clean_password2(self):
        # 检查两个密码条目匹配
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码不匹配")
        return password2

    def save(self, commit=True):
        #保存密码散列的格式提供
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

#重写admin
class UserChangeForm(forms.ModelForm):
    """
    更新用户的一种形式。
    包括所有字段用户,
    但取代了管理员的密码字段密码散列显示领域。
    """
    password = ReadOnlyPasswordHashField(label="Password",
        help_text=("原始密码不存储,所以没有办法看到"
                    "这个用户的密码,但是你可以改变密码 "
                    "使用 <a href=\"../password/\">修改密码</a>."))#哈值

    class Meta:
        model = UserProfile
        fields = ('email', 'password', 'name', 'is_active', 'is_superuser')

    def clean_password(self):
        # 不管用户提供什么,返回初始值。
        # 这是在这里,而不是在球场上,因为
        # 字段没有对初始值的访问
        return self.initial["password"]

#重写admin
class UserProfileAdmin(UserAdmin):#用户类,继承上一个类 UserAdmin
    # 单添加和更改用户实例
    form = UserChangeForm
    add_form = UserCreationForm

    # 字段用于显示用户模型。
    # 这些覆盖定义UserAdmin固定在底座上
    # auth.User引用特定字段。
    list_display = ('email', 'name','is_active', 'is_superuser', ) #显示字段表头
    list_filter = ('is_superuser',) # 过滤器(可以包含ManyToManyField) （注意加 逗号 , ）
    fieldsets = (                 #自定义显示字段
        (None, {'fields': ('email','name', 'password')}),
        # ('个人信息', {'fields': ( 'email','name')}),
        ('用户权限', {'fields': ('is_active','is_superuser','groups','user_permissions')}),#后台显示配置
    )
    #添加自定义字段
    # 覆盖get_fieldsets时使用这个属性创建一个用户。
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',) #搜索(不能包含CharField)（注意加 逗号 , ）
    ordering = ('email',) #自定义排序，默认'-id'
    filter_horizontal = ('groups','user_permissions', ) #复选框


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'qq', 'source', 'consultant', 'content', 'date']
    list_filter = ('source','consultant','consult_courses',)
    list_per_page = 2
    search_fields = ('name', 'qq')

    actions = []#定制功能    #测试返回到一个新页面

#注册到 Django Admin里
admin.site.register(models.Branch)                  #01校区表
admin.site.register(models.ClassList)               #02班级表
admin.site.register(models.Course)                  #03课程表，可以报名那些课程
admin.site.register(models.Customer, CustomerAdmin)                #04客户信息表
admin.site.register(models.CustomerFollowUp)        #05客户跟进表
admin.site.register(models.Enrollment)              #06学员报名信息表
admin.site.register(models.Payment)                 #07缴费记录表
admin.site.register(models.CourseRecord)            #08每节课上课纪录表
admin.site.register(models.StudyRecord)             #09学习纪录
# admin.site.register(models.UserProfile)             #10账号表
# 现在注册这个新UserAdmin ,因为我们不在使用Django的内置权限
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(models.Role)                    #11角色表
admin.site.register(models.Tag)                     #12标签表
