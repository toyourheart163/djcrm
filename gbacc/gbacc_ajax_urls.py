# gbacc_ajax_urls.py


# ————————42PerfectCRM实现AJAX全局账号注册————————
from django.conf.urls import url
from gbacc import gbacc_ajax_views
urlpatterns = [
    url(r'^gbacc_ajax_register/', gbacc_ajax_views.gbacc_ajax_register, name='gbacc_ajax_register'),  # ajax注册

    # ————————43PerfectCRM实现AJAX全局账号登陆————————
    url(r'^gbacc_ajax_login/', gbacc_ajax_views.gbacc_ajax_login, name='gbacc_ajax_login'),  # 全局登录
    url(r'^gbacc_fast_login/', gbacc_ajax_views.gbacc_fast_login, name='gbacc_fast_login'),
    # LOGIN_URL = '/gbacc/gbacc_login/'# login_url 配置，默认'/accounts/login/' #注意 / （斜杠，绝对路径）#settings.py
    # ————————43PerfectCRM实现AJAX全局账号登陆————————
]
# ————————42PerfectCRM实现AJAX全局账号注册————————

# gbacc_ajax_urls.py