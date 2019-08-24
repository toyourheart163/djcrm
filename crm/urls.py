from django.urls import path, re_path

from crm import views

urlpatterns = [
    re_path(r'^customer/(\d+)/enrollment/$', views.enrollment, name="enrollment"),
    re_path(r'^customer/registration/(\d+)/(\w+)/$', views.stu_registration, name="stu_registration"),  # 报名流程二 学员签同合
    re_path(r'^contract_prompt/$', views.contract_prompt, name="contract_prompt"),  # 报名流程二 提示学员
    re_path(r'^not_audit/$', views.not_audit, name="not_audit"),  # 报名流程二  未审核 查询
    re_path(r'^contract_review/(\d+)/$', views.contract_review, name="contract_review"),  # 报名流程三  审核
    re_path(r'^enrollment_rejection/(\d+)/$', views.enrollment_rejection, name="enrollment_rejection"),  # 报名流程三 驳回
    re_path(r'^not_payment/$', views.not_payment, name="not_payment"),  # 报名流程四  未 缴费 查询
    re_path(r'^already_payment/$', views.already_payment, name="already_payment"),  # 报名流程四  已 缴费 查询
    re_path(r'^payment/(\d+)/$', views.payment, name="payment"),  # 报名流程四    缴费   #财务

    re_path(r'^student_course/$', views.student_course, name='student_course'),   #学生报名的课程
    re_path(r'^studyrecords/(\d+)/$', views.studyrecords, name='studyrecords'),  # #学生上课记录列表StudyRecord
    re_path( r'^homework_detail/(\d+)/(\d+)/$', views.homework_detail, name='homework_detail' ),
    re_path(r'^teacher_class/$', views.teacher_class,name='teacher_class'),#讲师班级
    re_path(r'^teacher_class_detail/(\d+)/$', views.teacher_class_detail, name='teacher_class_detail'),  # 讲师班级课节详情
    re_path( r'^teacher_lesson_detail/(\d+)/(\d+)/$', views.teacher_lesson_detail,name='teacher_lesson_detail' ),  # 本节课的学员
    re_path( r'^homeworks/(\d+)/(\d+)/(\d+)/$', views.howk_down, name='howk_down' ),  # 作业下载

]
