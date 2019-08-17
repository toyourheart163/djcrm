#app_config.py
from django import conf #配置文件

def kingadmin_auto_discover():
    for app in conf.settings.INSTALLED_APPS:
        try:
            #去每个app下面执行kingadmin.py文件
            mod = __import__('%s.kingadmin' % app)
            #打印每个app已注册的model名字
            print(mod.kingadmin)
        except ImportError as e:
            # print("app has no module kingadmin 不存在")
            pass