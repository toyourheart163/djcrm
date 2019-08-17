from django.contrib import admin
from django.shortcuts import render

# Register your models here.
from crm import models #从crm导入models

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
admin.site.register(models.UserProfile)             #10账号表
admin.site.register(models.Role)                    #11角色表
admin.site.register(models.Tag)                     #12标签表
