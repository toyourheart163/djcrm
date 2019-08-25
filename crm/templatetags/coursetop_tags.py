# coursetop_tags.py
# ————————64PerfectCRM实现CRM课程排名详情————————
from django import template

from crm import models

register = template.Library()

@register.simple_tag
def fetch_stu_course_score(class_grade_dic, enroll_obj_id ): #获取 学员 课程 分数
    score=class_grade_dic.get(enroll_obj_id) #根据 id 找对应的分数
    print('#{学员ID：分数} #全班成绩',score)
    return score

@register.simple_tag
def get_stu_grade_ranking(course_ranking_dic,enroll_obj_id):#得到 学员 班级 排名
    score_top = course_ranking_dic.get(enroll_obj_id) #根据id 找对应的排名
    if score_top:
        print('#{学员ID: [分数, 排名] } #全班排名:', score_top[1])
        return score_top[1]

@register.simple_tag
def get_already_homework(enroll_obj_id): #获得已交作业
    score_list=models.StudyRecord.objects.select_related().filter(student=enroll_obj_id).values_list('score')#根据09学习纪录的ID #获取学习成绩列表
    number=0
    for score in score_list:
        if score!= (0,) :
            number += 1
    print('已交作业次数',number)
    return number


@register.simple_tag
def get_stu_attendance(enroll_obj_id): #获得学员出勤次数
    attendance_list=models.StudyRecord.objects.select_related().filter(student=enroll_obj_id).values_list('attendance')
    number=0
    for attendance in attendance_list:
        if attendance == (0,) :
            number += 1
    print('获得点名出勤',number)
    return number

@register.simple_tag
def get_stu_late(enroll_obj_id): #获得学员迟到次数
    attendance_list=models.StudyRecord.objects.select_related().filter(student=enroll_obj_id).values_list('attendance')
    number=0
    for attendance in attendance_list:
        if attendance == (1,) :
            number += 1
    print('获得点名迟到',number)
    return number

@register.simple_tag
def get_stu_absenteeism(enroll_obj_id): #获得学员缺勤次数
    attendance_list=models.StudyRecord.objects.select_related().filter(student=enroll_obj_id).values_list('attendance')
    number=0
    for attendance in attendance_list:
        if attendance == (2,) :
            number += 1
    print('获得点名缺勤',number)
    return number

@register.simple_tag
def get_stu_early(enroll_obj_id): #获得学员早退次数
    attendance_list=models.StudyRecord.objects.select_related().filter(student=enroll_obj_id).values_list('attendance')
    number=0
    for attendance in attendance_list:
        if attendance == (3,) :
            number += 1
    print('获得点名早退',number)
    return number

@register.simple_tag
def id_enrollment(enroll_obj):#ID查姓名
    enrollment = models.Enrollment.objects.filter(id=enroll_obj).first()#通过学员ID查06学员报名信息表
    return enrollment #06学员报名信息表

# coursetop_tags.py