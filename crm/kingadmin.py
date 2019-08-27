from django.shortcuts import render
from django.forms import ValidationError

from crm import models
from king_admin.base_admin import site,BaseAdmin

class UserProfileAdmin(BaseAdmin):#定制Djanago admin
    list_display = ('id', 'email', 'name')  # 显示字段表头
    readonly_fields = ('password',)   # 不可修改，限制
    filter_horizontal = ('user_permissions', 'groups','roles')  # 复选框
    exclude=['last_login']

site.register(models.UserProfile, UserProfileAdmin)

class BranchAdmin(BaseAdmin):
    list_display = ('id', 'name')

site.register(models.Branch, BranchAdmin)
# 02班级表
class ClassListAdmin(BaseAdmin):
    list_display = ['id', 'branch', 'course', 'class_type', 'semester', 'start_date', 'end_date']  # 显示字段表头
    list_filter = ['branch', 'course', 'class_type']  # 过滤器(可以包含ManyToManyField) （注意加 逗号 , ）
    filter_horizontal = ['teachers']  #复选框

site.register(models.ClassList,ClassListAdmin)               #02班级表

#04客户信息表
class CustomerAdmin(BaseAdmin):#定制Djanago admin
    list_display = ('id', 'contact_type', 'contact', 'source', 'consultant', 'content', 'date','status','enroll')  # 显示字段表头
    list_per_page = 10
    list_filter = ('date', 'source','consultant','consult_courses',)
    search_fields = ('name', 'contact')
    actions = []#定制功能    #测试返回到一个新页面
    ordering = '-qq'
    filter_horizontal = ('tags',)
    readonly_fields = ('qq', 'consultant',)
    readonly_table = True

    colored_fields = {
        'status':{'已报名':"rgba(145, 255, 0, 0.78)",
                  '未报名':"#ddd"},}

    def enroll(self):
        '''报名'''
        print("customize field enroll",self)
        link_name = "报名"
        if self.instance.status == 0:
            link_name = "报名新课程"
        return '''<a target="_blank" class="btn-link" href="/crm/customer/%s/enrollment/">点击%s</a> ''' % (self.instance.id,link_name)
                # url(r'^customer/(\d+)/enrollment/$', sales_views.enrollment, name="enrollment"),  # 客户招生#报名流程一 下一步
                # target属性用于表示所链接文件打开到的位置 #记住，“”内的文字只是表示一个对象的名子。
    
    enroll.display_name = "报名链接"

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

# 06学员报名信息表
class EnrollmentAdmin(BaseAdmin):  # 定制Djanago admin
    list_display = ('id', 'customer', 'enrolled_class', 'consultant', 'Pay_cost', 'date', 'payment')  # 显示字段表头
    colored_fields = {
        'Pay_cost': {True: "rgba(145, 255, 0, 0.78)",
                     False: "#ddd"}, }
    def payment(self):
        link_name = "增加缴费"
        if self.instance.Pay_cost == False:
            link_name = "缴费"
        return '''<a target="_blank" class="btn-link"  href="/crm/payment/%s/" >点击%s</a> ''' % (self.instance.id, link_name)
        # url(r'^payment/(\d+)/$', financial_views.payment, name="payment"),  # 报名流程四    缴费   #财务
        # target属性用于表示所链接文件打开到的位置 #记住，“”内的文字只是表示一个对象的名子。
    payment.display_name = "缴费链接"

class StudyRecordAdmin(BaseAdmin):
    list_display = ('id', 'score')

site.register(models.Customer,CustomerAdmin)
site.register(models.Enrollment, EnrollmentAdmin)  # 06学员报名信息表
site.register(models.CourseRecord)
site.register(models.StudyRecord, StudyRecordAdmin)

# 11角色表
class RoleAdmin(BaseAdmin):
    list_display = ['id', 'name']  # 显示字段表头
    filter_horizontal = ['menus']  # 复选框

# 13一层菜单名
class FirstLayerMenuAdmin(BaseAdmin):
    list_display = ['id', 'name', 'url_type', 'url_name', 'order']  # 显示字段表头

# 14二层菜单名
class SubMenuMenuAdmin(BaseAdmin):
    list_display = ['id', 'name', 'url_type', 'url_name', 'order']  # 显示字段表头

site.register(models.Role,RoleAdmin) #11角色表
site.register(models.FirstLayerMenu,FirstLayerMenuAdmin)  #13一层菜单名
site.register(models.SubMenu,SubMenuMenuAdmin)   #14二层菜单名

class GroupsAdmin(BaseAdmin):
    list_display = ['id', 'name']  # 显示字段表头
    filter_horizontal = ['permissions']  # 复选框
site.register(models.Groups,GroupsAdmin)   #14二层菜单名