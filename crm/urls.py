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
]