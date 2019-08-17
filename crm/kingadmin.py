from django.shortcuts import render

from crm import models

from king_admin.base_admin import site,BaseAdmin


#04客户信息表
class CustomerAdmin(BaseAdmin):#定制Djanago admin
    list_display = ('id', 'qq', 'source', 'consultant', 'content', 'date')  # 显示字段表头
    list_per_page = 8
    list_filter = ('date', 'source','consultant','consult_courses',)
    search_fields = ('name', 'qq')
    actions = []#定制功能    #测试返回到一个新页面
    ordering = '-qq'
    

site.register(models.Customer,CustomerAdmin)
site.register(models.CourseRecord)
