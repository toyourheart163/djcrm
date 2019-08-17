from django import template #模板
register = template.Library() #模板库

@register.simple_tag
#Django中利用filter与simple_tag为前端自定义函数的实现方法
def get_model_verbose_name(model_obj):
    model_name = model_obj._meta.verbose_name_plural if model_obj._meta.verbose_name else model_obj._meta.verbose_name_plural
    if not model_name:
        model_name = model_obj._meta.model_name
    return model_name

@register.simple_tag
def get_model_name(model_obj):
    return model_obj._meta.model_name

@register.simple_tag
def get_app_name(model_obj):
    return model_obj._meta.app_label

from django.utils.safestring import mark_safe
#使用mark_safe函数标记后，django将不再对该函数的内容进行转义

@register.simple_tag
def build_table_row(admin_obj,obj):
    row_ele = "" #为了生成一整行返回前端
    if admin_obj.list_display:
        #如果不为空，有在crm/kingadmin.py注册site.register(models.Customer,CustomerAdmin)
        for column in admin_obj.list_display: #循环base_admin里class BaseAdmin下list_display = ()
            column_obj = obj._meta.get_field(column)#遍历获取  传进的参数对象

            if column_obj.choices:#判断如果字段有choices属性
                #获取choices的字符串（外健）
                get_column_data = getattr(obj,"get_%s_display" % column) #反射，传进的参数对象，拼接字段
                column_data = get_column_data()#函数，拿到数据
            else:
                column_data = getattr(obj, column)#反射，

            td_ele = '''<td>%s</td>''' % column_data  #把反射来的值 拼接字符串 生成<td>
            row_ele += td_ele    #把 <td>  拼接到上面到空字符串
    else:
        row_ele +="<td>%s</td>" %obj  #把<td>拼接到上面到空字符串,crm/models.py里 def __str__(self):的返回值
    return mark_safe(row_ele) #使用mark_safe函数标记后，django将不再对该函数的内容进行转义

