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
def display_all_related_obj(objs):
    # 取出对象及所有相关联的数据
    from django.db.models.query import QuerySet
    if type(objs) != QuerySet:
        objs = [objs, ]
    if objs:
        model_class = objs[0]._meta.model  # 取表对象
        model_name = objs[0]._meta.model_name  # 取表名
        return mark_safe(recursive_related_objs_lookup(objs))

# <-----------------递归获取映射关系--------------------------------
def recursive_related_objs_lookup(objs, name=None, conn_batch_size=0):
    name = set()
    print(name)
    print('传递过来的objs:', objs)
    # 开始标签的拼接
    ul_ele = "<ul style='color: blue'>"
    for obj in objs:
        li_ele = '''<li>{0}:{1}</li>'''.format(obj._meta.verbose_name, obj.__str__().strip("<>"))
        print('str:', obj.__str__(), '类型:', type(obj.__str__()))
        print('关联的表的自定表名:', li_ele)
        ul_ele += li_ele
        print('拼接li_ele:', ul_ele)
        # 映射关系处理
        # <---------------------------特殊关联处理-----------------------------------
        # 多对多关系
        for m2m_field in obj._meta.local_many_to_many:  # local_many_to_many返回列表，many_to_many返回元祖
            print('--开始循环反射-多对多-关系处理--')
            sub_ul_ele = "<ul style='color: red'>"
            m2m_field_obj = getattr(obj, m2m_field.name)  # 反射 如果有选项
            print('反射选项:', m2m_field_obj)

            for m2m_data in m2m_field_obj.select_related():
                print('开始循环多对多标签拼接:', m2m_data)

                sub_li_ele = '''<li>{0}:{1}</li>'''.format(m2m_field.verbose_name, m2m_data.__str__().strip("<>"))
                sub_ul_ele += sub_li_ele
            sub_ul_ele += '</ul>'
            ul_ele += sub_ul_ele
            print('生成完整 多对多 标签..:', ul_ele)
        # <---------------------------外健关联处理------------------------------------
        for related_obj in obj._meta.related_objects:
            print('--开始-外健关联-处理--')
            if hasattr(obj, related_obj.get_accessor_name()):
                print('--判断对象中是否包含反查属性--')
                accessor_obj = getattr(obj, related_obj.get_accessor_name())
                print('获取反查对应的对象: ')
                if hasattr(accessor_obj, 'select_related'):
                    print('--判断有没有获取数据的方法或属性-- ')
                    target_object = accessor_obj.select_related()
                    print('获取数据的方法或属性: ', target_object)

                    if 'ManyToManyRel' in related_obj.__repr__():
                        print('--开始-外健关联-多对多-处理--.')

                        # 生成UL
                        sub_ul_ele = '<ul style="color: green">'
                        for data in target_object:
                            print('开始循环-外健关联-标签拼接...', data)
                            sub_li_ele = '''<li>{0}:{1}</li>'''.format(data._meta.verbose_name,
                                                                       data.__str__().strip("<>"))
                            sub_ul_ele += sub_li_ele
                        sub_ul_ele += '</ul>'
                        ul_ele += sub_ul_ele
                        print('-外健关联-生成完整标签:', ul_ele)
                    # <---------------递归处理-------------------
                    if len(target_object) != conn_batch_size:
                        print('--有下级对象存在,进行-递归-循环--')
                        names = target_object.__str__()
                        print(names, type(names))
                        if names == name:
                            print('--如果是自己关联自己，就不递归了--')
                            ul_ele += '</ul>'
                            return ul_ele
                        else:
                            print('--防止无限递归+1--')
                            conn_batch_size = conn_batch_size + 1
                            node = recursive_related_objs_lookup(target_object, name=names,
                                                                 conn_batch_size=conn_batch_size)
                            ul_ele += node

                    # <---------------由于使用递归，下面的标签样会发生重复，就不需要使用了--------------------
                else:
                    print('外健关联 一对一:', accessor_obj)
                    target_object = accessor_obj
                    print("外健关联 一对一：", target_object, '属性：', type(target_object))

    ul_ele += '</ul>'
    return ul_ele

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