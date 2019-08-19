from django.shortcuts import render
from django.forms import ValidationError

from crm import models
from king_admin.base_admin import site,BaseAdmin

class UserProfileAdmin(BaseAdmin):#定制Djanago admin
    list_display = ('id', 'email', 'name')  # 显示字段表头
    readonly_fields = ('password',)   # 不可修改，限制
    filter_horizontal = ('user_permissions','groups') #复选框
    exclude=['last_login']

site.register(models.UserProfile, UserProfileAdmin)

#04客户信息表
class CustomerAdmin(BaseAdmin):#定制Djanago admin
    list_display = ('id', 'qq', 'source', 'consultant', 'content', 'date')  # 显示字段表头
    list_per_page = 8
    list_filter = ('date', 'source','consultant','consult_courses',)
    search_fields = ('name', 'qq')
    actions = []#定制功能    #测试返回到一个新页面
    ordering = '-qq'
    filter_horizontal = ('tags',)
    readonly_fields = ('qq', 'consultant',)
    readonly_table = True

    def default_form_validation(self,obj):
        print('validation:制定的',obj.cleaned_data)
        consult_course=obj.cleaned_data.get('content','')#自制验证字段
        if len(consult_course)<10:
            return ValidationError(#添加错误信息 返回
                                ("该字段%(field)s 咨询内容记录不能少于10个字符"),
                                code='invalid',
                                params={'field':'content',},
                            )

    def clean_name(self,obj,*args,**kwargs):#名称验证 单个
        name=obj.cleaned_data['name']
        if not name:
            obj.add_error('name','不能为空!')
            return ValidationError(#添加错误信息 返回
                                ("%(field)s:该字段 不能为空"),
                                code='invalid',
                                params={'field':'name',},
                            )
        elif len(name)<5:
            obj.add_error('name','不能小于5个字符!')
            #return ValidationError('',)
            return ValidationError(#添加错误信息 返回
                                ("%(field)s:该字段 不能小于5个字符!"),
                                code='invalid',
                                params={'field':'name',},
                            )

site.register(models.Customer,CustomerAdmin)
site.register(models.CourseRecord)
