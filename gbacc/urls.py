# gbacc_urls.py
# ————————38PerfectCRM实现全局账号登录注销————————
from django.urls import path, re_path
from gbacc import views
urlpatterns = [
    re_path(r'^gbacc_login/', views.gbacc_login, name='gbacc_login'),  # 全局登录
    # LOGIN_URL = '/gbacc/gbacc_login/'# login_url 配置，默认'/accounts/login/' #注意 / （斜杠，绝对路径）#settings.py

    re_path(r'^gbacc_logout/', views.gbacc_logout, name='gbacc_logout'),  # 全局注销,默认跳转到accounts/login
    re_path(r'^check_code.html/$', views.check_code, name='check_code'),
    re_path(r'^gbacc_register/', views.gbacc_register, name='gbacc_register'),
    re_path(r'^(\d+)/gbacc_modify/$', views.gbacc_modify, name='gbacc_modify'),
    
]
# ————————38PerfectCRM实现全局账号登密码密码录注销————————

# gbacc_urls.py