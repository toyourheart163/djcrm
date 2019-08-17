#base_admin.py
#Django admin 注册功能的形式
# sites = {
#     'crm':{
#         'customers':CustomerAdmin,
#         'customerfollowup':CustomerFollowUPAdmin,
#     }
# }

class AdminRegisterException(Exception):  #自定义异常
    def __init__(self,msg):
        self.message = msg

class BaseAdmin(object):#自定义方法
    list_display = ()

class AdminSite(object):
    def __init__(self):
        self.registered_sites = {}   #传到views 里调用

    def register(self,model,admin_class=None): #默认值None 使用 BaseAdmin
        app_name = model._meta.app_label#用内置方法获取 APP名字 （crm）
        model_name = model._meta.model_name#用内置方法获取 表名  (Customer)
        if app_name not in self.registered_sites:
            self.registered_sites[app_name] = {} #创建  crm={}
        if model_name in self.registered_sites[app_name]:
            raise AdminRegisterException("app [%s] model [%s] has already registered!异常"
                                                 %(app_name,model_name))#自定义异常，
        if not admin_class:
            admin_class = BaseAdmin  #默认值None 使用 BaseAdmin
        admin_class.model = model
        self.registered_sites[app_name][model_name] = admin_class #注册APP

site = AdminSite() #实例化类  单例模式
