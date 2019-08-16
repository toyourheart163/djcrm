#app_config.py
from django import conf #配置文件

for app in conf.settings.INSTALLED_APPS:
    try:
        print("import ",__import__("%s.kingadmin" % app))
    except ImportError as e:
        print("app has no module kingadmin 不存在")
