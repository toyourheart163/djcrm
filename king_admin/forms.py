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

    def __new__(cls, *args, **kwargs):
        # print("base fields",cls.base_fields)
        # 字段名    #字段数据
        for field_name, field_obj in cls.base_fields.items():
            # print(field_name,dir(field_obj))
            field_obj.widget.attrs['class'] = 'form-control'  # 前端的样式
            # field_obj.widget.attrs['maxlength'] = getattr(field_obj,'max_length' ) if hasattr(field_obj,'max_length') \
            #     else ""
        return forms.ModelForm.__new__(cls)
    dynamic_model_form = type("DynamicModelForm", (forms.ModelForm,), {"Meta": Meta})  # 生成modelform的类,
    setattr(dynamic_model_form, "__new__", __new__)
    # ————————20PerfectCRM实现King_admin数据修改美化————————

    return dynamic_model_form