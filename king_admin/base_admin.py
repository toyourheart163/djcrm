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

registered_sites={}
def register(model,admin_class=None): #默认值None 使用 BaseAdmin
    app_name = model._meta.app_label#用内置方法获取 APP名字 （crm）
    model_name = model._meta.model_name#用内置方法获取 表名  (Customer)
    if app_name not in registered_sites:
        registered_sites[app_name] = {} #创建  crm={}
    if model_name in registered_sites[app_name]:
        raise AdminRegisterException("app [%s] model [%s] has already registered!异常"
                                             %(app_name,model_name))#自定义异常
    if not admin_class:
        admin_class = BaseAdmin  #默认值None 使用class BaseAdmin
    registered_sites[app_name][model_name] = admin_class #注册APP
