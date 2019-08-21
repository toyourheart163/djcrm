# forms.py
# ————————47PerfectCRM实现CRM客户报名流程————————
from django.forms import ModelForm  #继承forms自定制

from crm import models  #数据库
#报名 销售填写
class EnrollmentForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = 'form-control'## 前端的样式
        return ModelForm.__new__(cls)
    class Meta:
        model= models.Enrollment
        fields= ['enrolled_class']
# ————————47PerfectCRM实现CRM客户报名流程————————

#报名学员填 写
class CustomerForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = 'form-control'## 前端的样式
            if field_name in cls.Meta.readonly_fields:#如果不可修改
                field_obj.widget.attrs['disabled'] = True## 前端的样式 灰色
        return ModelForm.__new__(cls)

    def clean_qq(self):
        #print(self.instance.qq,self.cleaned_data['qq'],'9696969696')
        if self.instance.qq != self.cleaned_data['qq']:  #输入的值和 cleaned_data的值
            self.add_error('qq',"大神，请勿非法修改！")
        return self.cleaned_data['qq']

    def clean_consultant(self):
        if self.instance.consultant != self.cleaned_data['consultant']:
            self.add_error('consultant',"非法修改！不要尝试！")
        return self.cleaned_data['consultant']

    def clean_source(self):
        if self.instance.source != self.cleaned_data['source']:
            self.add_error('source',"非法修改！不能通过！")
        return self.cleaned_data['source']
        
    class Meta:
        model=models.Customer#客户表
        fields='__all__'
        exclude=['tags','content','memo','status','referral_from','consult_courses']#排除，不显示
        readonly_fields=['qq','consultant','source']#不可修改
# ————————48PerfectCRM实现CRM客户报名流程学生合同————————

#缴费记录
class PaymentForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = 'form-control'## 前端的样式
        return ModelForm.__new__(cls)
    class Meta:
        model=models.Payment
        fields='__all__'