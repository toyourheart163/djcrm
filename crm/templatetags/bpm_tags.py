# bpm_tags.py

# ————————48PerfectCRM实现CRM客户报名流程学生合同————————
from django import template
register = template.Library()    #模板库

#合同格式
@register.simple_tag
def render_enrolled_contract(enroll_obj):#合同格式
    if enroll_obj.enrolled_class.contract.template:
        return enroll_obj.enrolled_class.contract.template.format(course_name=enroll_obj.enrolled_class,stu_name=enroll_obj.customer.name)
    else:
        return ''

# ————————48PerfectCRM实现CRM客户报名流程学生合同————————

# bpm_tags.py

# bpm_tags.py