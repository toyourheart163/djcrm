from crm import models

from king_admin.base_admin import register,BaseAdmin

#04客户信息表
class CustomerAdmin(BaseAdmin):#定制Djanago admin
    list_display = ('id', 'qq', 'source', 'consultant', 'content', 'date')  # 显示字段表头

register(models.Customer,CustomerAdmin)
register(models.CourseRecord)
