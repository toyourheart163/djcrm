#kingadmin_tags.py

from django import template #模板
register = template.Library() #模板库

@register.simple_tag #Django中利用filter与simple_tag为前端自定义函数的实现方法
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

from django.utils.safestring import mark_safe #使用mark_safe函数标记后，django将不再对该函数的内容进行转义

@register.simple_tag
def build_table_row(admin_obj,obj):#通过kingadmin_tags在后台处理 再传到前端
    row_ele = "" #为了生成一整行返回前端
    if admin_obj.list_display:#如果不为空，有在crm/kingadmin.py注册site.register(models.Customer,CustomerAdmin)
        #循环所有 要显示 的字符串 进行反射 展示 字段
        for index, column in enumerate(admin_obj.list_display): #循环base_admin里class BaseAdmin下list_display = ()
            column_obj = obj._meta.get_field(column)#遍历获取  传进的参数对象

            if column_obj.choices:#判断如果字段有choices属性
                #获取choices的字符串（外健）
                get_column_data = getattr(obj,"get_%s_display" % column) #反射，传进的参数对象，拼接字段
                column_data = get_column_data()#函数，拿到数据
            else:
                column_data = getattr(obj, column)#反射，
            # ————————10PerfectCRM实现King_admin日期优化————————
            if type(column_data).__name__ == 'datetime':
                column_data = column_data.strftime('%Y-%m-%d %H-%M-%S')
            # ————————10PerfectCRM实现King_admin日期优化————————
            if index == 0: #首列
                # 生成一个链接 跳转到编辑页面        #Format参数是一个格式字符串(%s升级版)
                td_ele = '''<td><a href="/king_admin/{app_name}/{model_name}/{obj_id}/change/">{column_data}</a> </td>'''\
                            .format(app_name=admin_obj.model._meta.app_label,
                                    model_name=admin_obj.model._meta.model_name,
                                    obj_id=obj.id,
                                    column_data=column_data)
            else:
                td_ele = '''<td>%s</td>''' % column_data  #把反射来的值 拼接字符串 生成<td>
            row_ele += td_ele    #把 <td>  拼接到上面到空字符串
    else:
        row_ele +="<td>%s</td>" %obj  #把<td>拼接到上面到空字符串,crm/models.py里 def __str__(self):的返回值
    return mark_safe(row_ele) #使用mark_safe函数标记后，django将不再对该函数的内容进行转义
# ————————09PerfectCRM实现King_admin显示注册表的内容————————

@register.simple_tag
def generate_filter_url(admin_obj): #拼接URL
    url = ''
    for k,v in admin_obj.filter_condtions.items():
        url += "&%s=%s" %(k,v )
    return url

#分页的省略显示
@register.simple_tag
def pag_omit(request,admin_obj):#传入当前页面值
    rest=''#大字符串
    order_by_url = generate_order_by_url(request)  # 排序
    filters = generate_filter_url(admin_obj)  # 分页
    add_tags=False#标志位
    for pages in admin_obj.querysets.paginator.page_range:
        #   前两页    或   后  两页                                       或    当前页的前后页
        if pages < 3 or pages>admin_obj.querysets.paginator.num_pages -2 or abs(admin_obj.querysets.number -pages) <=2:
            #样式
            add_tags=False
            ele_class=''  #颜色
            if pages == admin_obj.querysets.number: #--如果是当前页码,颜色加深 不进链接跳转--
                ele_class="active"    #颜色加深
            rest+='''<li class="%s"><a href="?page=%s%s%s">%s<span class="sr-only">(current)</span></a></li>'''\
                    %(ele_class,pages,order_by_url,filters,pages)
            # ————————17PerfectCRM实现King_admin单列排序————————

        else:#其他的用省略号表示
            if add_tags==False:#如果不是标志位的页面
                rest+='<li><a>...</a></li>'
                add_tags=True#标志位为真
    return mark_safe(rest)  #使用mark_safe函数标记后，django将不再对该函数的内容进行转义

from django.utils.timezone import datetime,timedelta

@register.simple_tag
def get_filter_field (filter_column,admin_obj):
    select_ele = """<select name='{filter_column}'><option  value="">---------</option>""" #标签 字符串 #拼接成下拉框返回
    field_obj = admin_obj.model._meta.get_field(filter_column)#调用内置方法
    selected = ''
    if field_obj.choices:
        for choice_item in field_obj.choices:
            if admin_obj.filter_condtions.get(filter_column) == str(choice_item[0]):
                selected = "selected"
            select_ele  +=  """<option value="%s" %s>%s</option> """ % (choice_item[0], selected, choice_item[1])
            selected = ""

    if type(field_obj).__name__ in "ForeignKey":
        for choice_item in field_obj.get_choices()[1:]:
            if admin_obj.filter_condtions.get(filter_column)== str(choice_item[0]):  # 就是选择的这个条件，整数转字符串
                selected = "selected"
            select_ele += """<option value="%s" %s>%s</option> """ % (choice_item[0], selected, choice_item[1])
            selected=''

    if type(field_obj).__name__ in ['DateTimeField', 'DateField']:  # 如果是时间格式
        date_els = []  # 日期条件项
        today_ele = datetime.now().date()  # 今天日期
        date_els.append(['今天', today_ele])  # 今天
        date_els.append(['昨天', today_ele - timedelta(days=1)])  # 昨天
        date_els.append(['近7天', today_ele - timedelta(days=7)])  # 一周
        date_els.append(['近30天', today_ele - timedelta(days=30)])  # 三十
        date_els.append(['本月', today_ele.replace(day=1)])  # 本月
        date_els.append(['近90天', today_ele - timedelta(days=90)])  # 90天
        date_els.append(['近365天', today_ele - timedelta(days=365)])  # 365天
        date_els.append(['本年', today_ele.replace(month=1, day=1)])  ##今年

        for choice_item in date_els:
            if admin_obj.filter_condtions.get("%s__gte" %filter_column)==str(choice_item[1]):
                selected = 'selected'
            select_ele += """<option value="%s" %s>%s</option> """ % (choice_item[1], selected, choice_item[0])
            selected = ''
        filter_column_name = "%s__gte" %filter_column
    else:
        filter_column_name = filter_column

    select_ele += "</select>"
    select_ele=select_ele.format(filter_column=filter_column_name)#格式化时间的判断条件
    return mark_safe(select_ele)
# ————————16PerfectCRM实现King_admin日期过滤————————

# ————————17PerfectCRM实现King_admin单列排序————————
# kingadmin排序功能
@register.simple_tag
def  get_orderby_key(request,column):
    current_order_by_key = request.GET.get("_o")
    search_key = request.GET.get("_q")
    if search_key != None:
        if current_order_by_key != None: #如果不为空  #肯定有某列被排序了
            if current_order_by_key ==  column: # 判断是否相等 #当前这列正在被排序
                if column.startswith("-"): #startsWith是String类中的一个方法，用来检测某字符串是否以另一个字符串开始，返回值为boolean类型
                    return column.strip("-") #strip去掉  文本中句子开头与结尾的符号的
                else:
                    return "-%s&_q=%s" % (column, search_key)
        return "%s&_q=%s" % (column, search_key)
    else:
    # ————————18PerfectCRM实现King_admin搜索关键字————————
        if current_order_by_key != None: #如果不为空  #肯定有某列被排序了
            if current_order_by_key ==  column: # 判断是否相等 #当前这列正在被排序
                if column.startswith("-"): #startsWith是String类中的一个方法，用来检测某字符串是否以另一个字符串开始，返回值为boolean类型
                    return column.strip("-") #strip去掉  文本中句子开头与结尾的符号的
                else:
                    return "-%s"%column
        return column   #同上4句
# kingadmin排序功能

@register.simple_tag
def display_order_by_icon(request, column):
    current_order_by_key = request.GET.get("_o")
    if current_order_by_key != None: #肯定有某列被排序了
        if current_order_by_key.strip("-") == column: # 当前这列正在被排序  #strip去掉  文本中句子开头与结尾的符号的
            if current_order_by_key.startswith("-"): #startsWith是String类中的一个方法，用来检测某字符串是否以另一个字符串开始，返回值为boolean类型
                icon = "▲"
            else:
                icon = "▼"
            ele = """<i style='color: red'>%s</i>""" % icon
            return mark_safe(ele)
    return '' #防止出现 None
# kingadmin排序功能  显示排序图标

# kingadmin排序功能  # 过滤后排序功能 #}
@register.simple_tag
def get_current_orderby_key(request): #注意生成的URL问题
    #获取当前正在排序的字段名   #<input type="hidden" name="_o" value="{% get_current_orderby_key request %}">
    current_order_by_key = request.GET.get("_o")
    return current_order_by_key or ''
# kingadmin排序功能  # 过滤后排序功能 #}

# kingadmin排序功能   # 过滤后排序功能 # 排序分页
@register.simple_tag
def generate_order_by_url (request):
    current_order_by_key = request.GET.get("_o")
    if current_order_by_key != None:  # 肯定有某列被排序了
        return "&_o=%s" % current_order_by_key
    return ''

@register.simple_tag
def get_search_key(request):   #  搜索框里保留搜索值
    search_key = request.GET.get("_q")
    return search_key or ''

@register.simple_tag
def get_available_m2m_data(field_name, form_obj, admin_class):
    '''返回的是m2m字段关联表的所有数据'''
    #获取字段的对象
    field_obj = admin_class.model._meta.get_field(field_name)

    #consult_courses = models.ManyToManyField('Course',verbose_name='咨询课程')
    #consult_courses是一个m2m，通过consult_courses对象获取到Course（也就是获取到所有咨询的课程）
    obj_list = set(field_obj.related_model.objects.all())
    if form_obj.instance.id:
        selected_data = set(getattr(form_obj.instance, field_name).all())
        return obj_list - selected_data
    else:
        return obj_list

@register.simple_tag
def get_selected_m2m_data(field_name,form_obj,admin_class):
    '''返回已选的m2m数据'''
    #获取被选中的数据
    if form_obj.instance.id:
        selected_data = getattr(form_obj.instance,field_name).all()
        return selected_data
    return []

@register.simple_tag
def display_all_related_objs(obj):
    """
    显示要被删除对象的所有关联对象
    """
    ele = "<ul><b style='color:red'>%s</b>" % obj

    #获取所有反向关联的对象
    for reversed_fk_obj in obj._meta.related_objects:
        #获取所有反向关联对象的表名
        related_table_name =  reversed_fk_obj.name
        # 通过表名反向查所有关联的数据
        related_lookup_key = "%s_set" % related_table_name
        related_objs = getattr(obj,related_lookup_key).all()
        ele += "<li>%s<ul> "% related_table_name
        #get_internal_type(),获取字段的类型，如果是m2m，就不需要深入查找
        if reversed_fk_obj.get_internal_type() == "ManyToManyField":  # 不需要深入查找
            for i in related_objs:
                ele += "<li><a href='/kingadmin/%s/%s/%s/change/'>%s</a> 记录里与[%s]相关的的数据将被删除</li>" \
                       % (i._meta.app_label,i._meta.model_name,i.id,i,obj)
        #如果不是m2m，就递归查找所有关联的数据
        else:
            for i in related_objs:
                ele += "<li><a href='/kingadmin/%s/%s/%s/change/'>%s</a></li>" \
                    %(i._meta.app_label, i._meta.model_name,i.id,i)
                #递归查找
                ele += display_all_related_objs(i)
        ele += "</ul></li>"
    ele += "</ul>"
    return ele

@register.simple_tag
def get_admin_actions(admin_obj):
    #选择功能
    options = "<option class='form-control' value='-1'>-------</option>"#默认为空
    actions = admin_obj.actions #默认加自定制
    print('默认加自定制',actions)
    for action in actions:
        action_func = getattr(admin_obj,action)#功能方法  #反射
        if hasattr(action_func,"short_description"):#反射 如有自定义的名称执行函数方法
            action_name = action_func.short_description#等于自定义的名称 #显示中文
        else:
            action_name = action#等于函数名称
        options += """<option value="{action_func_name}">{action_name}</option> """.format(action_func_name=action, action_name=action_name)
    return mark_safe(options)

@register.simple_tag
def get_m2m_available_objs(admin_obj, field_name):
    '''返回m2m左侧所有待选数据'''
    # c= admin_obj.model.tags.rel.model.objects.all()
    # print('c',c)
    # m2m_objs= admin_obj.model.tags.rel.model.objects.all()
    # print('m2m_objs',m2m_objs)
    m2m_model = getattr(admin_obj.model, field_name).rel  # 复选框对象
    m2m_objs = m2m_model.model.objects.all()  # 获取到复选框所有内容
    return m2m_objs

# 复选 框内容已选中数据
@register.simple_tag
def get_m2m_chosen_objs(admin_obj, field_name, obj):
    """
    返回已选中的列表
    :param admin_obj:
    :param field_name:
    :param obj: 数据对象
    :return:
    """
    # print(["--->obj",obj])
    if obj.id:
        return getattr(obj, field_name).all()  # 返回所有的内容
    return [] 