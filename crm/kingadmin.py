from crm import models

from king_admin.base_admin import site,BaseAdmin

#04客户信息表
class CustomerAdmin(BaseAdmin):#定制Djanago admin
    list_display = ('id', 'qq', 'source', 'consultant', 'content', 'date')  # 显示字段表头

site.register(models.Customer,CustomerAdmin)
site.register(models.CourseRecord)
