# bpm_tags.py

# ————————48PerfectCRM实现CRM客户报名流程学生合同————————
from django import template
from django.db.models import Sum

register = template.Library()    #模板库

#合同格式
@register.simple_tag
def render_enrolled_contract(enroll_obj):#合同格式
    if enroll_obj.enrolled_class.contract.template:
        return enroll_obj.enrolled_class.contract.template.format(course_name=enroll_obj.enrolled_class,stu_name=enroll_obj.customer.name)
    else:
        return ''

#分数统计#我的成绩
@register.simple_tag
def get_score(enroll_obj,customer_obj):
    study_records=enroll_obj.studyrecord_set.filter(course_record__from_class_id=enroll_obj.enrolled_class.id)#根据班级ID 取09学习纪录的信息(包含'score')
    sum_score= study_records.aggregate(Sum('score'))  #aggregate #总 #返回一个字典,其中包含的计算(聚合) #Sum #合计值
    return sum_score
