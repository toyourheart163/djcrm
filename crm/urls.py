from django.urls import path, re_path

from crm import views

urlpatterns = [
    re_path(r'^customer/(\d+)/enrollment/$', views.enrollment, name="enrollment"),
    re_path(r'^customer/registration/(\d+)/$', views.stu_registration, name="stu_registration"),  # 报名流程二 学员签同合
]