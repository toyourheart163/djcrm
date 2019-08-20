# forms.py
# ————————19PerfectCRM实现King_admin数据修改————————
from django import forms
from crm import models

# class CustomerModelForm(forms.ModelForm):
#     class Meta: #调用内置方法
#         model = models.Customer  #获取表名
#         fields = "__all__"   #字段

def CreateModelForm(request,admin_obj):
    class Meta: #调用内置方法
        model = admin_obj.model  #获取表名
        fields = "__all__"   #字段
        exclude= admin_obj.exclude
    # ————————20PerfectCRM实现King_admin数据修改美化————————
        # type()就是一个最实用又简单的查看数据类型的方法。type()是一个内建的函数，调用它就能够得到一个反回值，从而知道想要查询的对像类型信息。
        # dynamic_model_form = type("DynamicModelForm", (forms.ModelForm,), {"Meta": Meta})  #生成modelform的类,
    # new()方法是在类准备将自身实例化时调用。new()方法始终都是类的静态方法，即使没有被加上静态方法装饰器。
    def __new__(cls, *args, **kwargs):
        # print("base fields",cls.base_fields)
        # 字段名    #字段数据
        for field_name, field_obj in cls.base_fields.items():
            # print(field_name,dir(field_obj))
            field_obj.widget.attrs['class'] = 'form-control'  # 前端的样式
            # field_obj.widget.attrs['maxlength'] = getattr(field_obj,'max_length' ) if hasattr(field_obj,'max_length') \
            #     else ""
            # ————————28PerfectCRM实现King_admin编辑限制————————
            if field_name in admin_obj.readonly_fields:#如果，在
                field_obj.widget.attrs['disabled'] = True
            # ————————28PerfectCRM实现King_admin编辑限制————————
        return forms.ModelForm.__new__(cls)
    # ————————28PerfectCRM实现King_admin编辑限制————————
    def default_clean(self):
        from django.forms import ValidationError
        error_list = []
        # ————————29PerfectCRM实现King_admin编辑自定义限制————————

        # ————————33PerfectCRM实现King_admin编辑整张表限制————————
        from django.utils.translation import ugettext as _  # 国际化
        if admin_obj.readonly_table: #在这后端验证，防止黑客添加
            raise ValidationError(#添加错误信息
                                    _("该表单不可修改!"),
                                    code='invalid',
                                )

        #给所有的form默认加一个 clean  验证
        print("default clean:",self)#得到整个form数据
        for field in admin_obj.readonly_fields:#循环获取crm/kingadmin.py里    readonly_fields = ('name','qq',)的数据
            print("readonly",field,self.instance)#获取到 字段名 ，对象（值）
            field_val_from_db  = getattr(self.instance,field)#获取数据库的值
            print("cleaned data:", self.cleaned_data)#获取到 前端的值
            field_val = self.cleaned_data.get(field)#获取到 前端的值
            if field_val_from_db == field_val:#数据库的值和前端的值对比
                print("数据库数据和前端数据一样 ")
            else: # 被篡改了
                self.add_error(field,' "%s" 是一个只读的字段,值应该是 "%s"！ 大神请不要篡改！！！'% (field, field_val_from_db))
    # ————————28PerfectCRM实现King_admin编辑限制————————
    dynamic_model_form = type("DynamicModelForm", (forms.ModelForm,), {"Meta": Meta})  # 生成modelform的类,
    setattr(dynamic_model_form, "__new__", __new__)
    # ————————20PerfectCRM实现King_admin数据修改美化————————
    # ————————28PerfectCRM实现King_admin编辑限制————————
    setattr(dynamic_model_form,"clean",default_clean)  #给所有的form默认加一个 clean  验证
    # ————————28PerfectCRM实现King_admin编辑限制———————
    return dynamic_model_form
# ————————19PerfectCRM实现King_admin数据修改————————

# forms.py