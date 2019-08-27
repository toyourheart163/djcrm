# CJ.py
# ————————74PerfectCRM实现CRM权限和权限组限制访问URL————————
import re #正则
from crm import models #数据库

# ————————01大类权限————————
#010201_只能查看校区表_GET
def JM_Branch(request,*args,**kwargs):
    url_path = request.path  # 获取URL
    url_list=re.findall('(\w+)',url_path) #正者表达式 获取参数
    url_model_name=url_list[2]
    model_name = 'branch'
    if url_model_name == model_name: #防止其他表通过权限
        return True
    else:
        return False

# 010301_只能查看班级表_GET
def JM_ClassList(request, *args, **kwargs):
    url_path = request.path  # 获取URL
    url_list = re.findall( '(\w+)', url_path )  # 正者表达式 获取参数
    url_model_name = url_list[2]
    model_name = 'classlist'
    if url_model_name == model_name:  # 防止其他表通过权限
        return True
    else:
        return False

# 010401_只能查看课程表_GET
def JM_Course(request, *args, **kwargs):
    url_path = request.path  # 获取URL
    url_list = re.findall( '(\w+)', url_path )  # 正者表达式 获取参数
    url_model_name = url_list[2]
    model_name = 'course'
    if url_model_name == model_name:  # 防止其他表通过权限
        return True
    else:
        return False

# 010501_只能查看客户表_GET
def JM_Customer(request, *args, **kwargs):
    url_path = request.path  # 获取URL
    url_list = re.findall( '(\w+)', url_path )  # 正者表达式 获取参数
    url_model_name = url_list[2]
    model_name = 'customer'
    if url_model_name == model_name:  # 防止其他表通过权限
        return True
    else:
        return False


#010601_只能查看跟进表_GET
def JM_CustomerFollowUp(request,*args,**kwargs):
    url_path = request.path  # 获取URL
    url_list=re.findall('(\w+)',url_path) #正者表达式 获取参数
    url_model_name=url_list[2]
    model_name = 'customerfollowup'
    if url_model_name == model_name: #防止其他表通过权限
        return True
    else:
        return False

# 010701_只能查看报名表_GET
def JM_Enrollment(request, *args, **kwargs):
    url_path = request.path  # 获取URL
    url_list = re.findall( '(\w+)', url_path )  # 正者表达式 获取参数
    url_model_name = url_list[2]
    model_name = 'enrollment'
    if url_model_name == model_name:  #防止其他表通过权限
        return True
    else:
        return False

# 010801_只能查看缴费表_GET
def JM_Payment(request, *args, **kwargs):
    url_path = request.path  # 获取URL
    url_list = re.findall( '(\w+)', url_path )  # 正者表达式 获取参数
    url_model_name = url_list[2]
    model_name = 'payment'
    if url_model_name == model_name:  #防止其他表通过权限
        return True
    else:
        return False


#010901_只能查看上课表_GET
def JM_CourseRecord(request,*args,**kwargs):
    url_path = request.path  # 获取URL
    url_list=re.findall('(\w+)',url_path) #正者表达式 获取参数
    url_model_name=url_list[2]
    model_name = 'courserecord'
    if url_model_name == model_name: #防止其他表通过权限
        return True
    else:
        return False


# 011001_只能查看学习表_GET
def JM_StudyRecord(request, *args, **kwargs):
    url_path = request.path  # 获取URL
    url_list = re.findall( '(\w+)', url_path )  # 正者表达式 获取参数
    url_model_name = url_list[2]
    model_name = 'studyrecord'
    if url_model_name == model_name:  #防止其他表通过权限
        return True
    else:
        return False


# 011101_只能查看账号表_GET
def JM_UserProfile(request, *args, **kwargs):
    url_path = request.path  # 获取URL
    url_list = re.findall( '(\w+)', url_path )  # 正者表达式 获取参数
    url_model_name = url_list[2]
    model_name = 'userprofile'
    if url_model_name == model_name:  #防止其他表通过权限
        return True
    else:
        return False


#011201_只能查看角色表_GET
def JM_Role(request,*args,**kwargs):
    url_path = request.path  # 获取URL
    url_list=re.findall('(\w+)',url_path) #正者表达式 获取参数
    url_model_name=url_list[2]
    model_name = 'role'
    if url_model_name == model_name: #防止其他表通过权限
        return True
    else:
        return False



#010301_只能查看班级表_GET
def JM_Tag(request,*args,**kwargs):
    url_path = request.path  # 获取URL
    url_list=re.findall('(\w+)',url_path) #正者表达式 获取参数
    url_model_name=url_list[2]
    model_name = 'tag'
    if url_model_name == model_name: #防止其他表通过权限
        return True
    else:
        return False


#011401_只能查看一层菜单_GET
def JM_FirstLayerMenu(request,*args,**kwargs):
    url_path = request.path  # 获取URL
    url_list=re.findall('(\w+)',url_path) #正者表达式 获取参数
    url_model_name=url_list[2]
    model_name = 'firstlayermenu'
    if url_model_name == model_name: #防止其他表通过权限
        return True
    else:
        return False


# 011501_只能查看二层菜单_GET
def JM_SubMenu(request, *args, **kwargs):
    url_path = request.path  # 获取URL
    url_list = re.findall( '(\w+)', url_path )  # 正者表达式 获取参数
    url_model_name = url_list[2]
    model_name = 'submenu'
    if url_model_name == model_name:  #防止其他表通过权限
        return True
    else:
        return False


#011601_只能查看权限组_GET
def JM_Groups(request,*args,**kwargs):
    url_path = request.path  # 获取URL
    url_list=re.findall('(\w+)',url_path) #正者表达式 获取参数
    url_model_name=url_list[2]
    model_name = 'groups'
    if url_model_name == model_name: #防止其他表通过权限
        return True
    else:
        return False

#011701_自己密码重置_GET
def own_password_reset(request,*args,**kwargs):
    url_path = request.path  # 获取URL 路径
    url_list = re.findall( '(\w+)', url_path )  # 正者表达式 获取参数
    url_model_name = url_list[4]    #字符串
    url_parameter =int(url_list[3])  #字符串转数字
    model_name = 'password_reset'  #字符串
    if url_model_name == model_name:  #防止其他表通过权限
        if url_parameter == request.user.id:  # 参数 等于 #当前登陆的ID
            return True
        else:
            return False
    else:
        return False
 # ————————01大类权限————————

 # ————————02大类权限————————
#020103_销售给自己的客户报名课程_GET
#销售 #客户招生#报名流程一 下一步
def own_enrollment(request,*args,**kwargs):
    url_path = request.path #获取URL 路径
    url_list=re.findall('(\w+)',url_path) #正者表达式 获取参数
    url_model_name= url_list[3]
    url_parameter =int(url_list[2])
    model_name = 'enrollment'
    if url_model_name==model_name: #防止其他表通过权限
        if request.user.id: #如果有ID
            list= request.user.customer_set.all()#获取ID 的客户表
            list_id=[]
            for obtain in list:#循环客户表ID
                results=obtain.id
                list_id.append(results)#生成列表
        if url_parameter in list_id: #对比URL参数 在不在 客户表ID里
            return True
        else:
            return False
    else:
        return False


#020107_销售给自己的客户审核合同_GET
#销售 # 报名流程三  审核
def own_contract_review(request,*args,**kwargs):
    url_path = request.path #获取URL 路径
    url_list=re.findall('(\w+)',url_path) #正者表达式 获取参数
    url_model_name= url_list[1]  #字符串
    url_parameter =int(url_list[2]) #字符串转数字
    model_name='contract_review' #字符串
    if url_model_name==model_name: #防止其他表通过权限
        if request.user.id: #如果有ID
            list= request.user.enrollment_set.all()#获取ID 的客户表
            list_id=[]  #数字列表
            for obtain in list:#循环客户表ID
                results=obtain.id
                list_id.append(results)#生成列表
        if url_parameter in list_id: #对比URL参数 在不在 列表里
            return True
        else:
            return False
    else:
        return False

# ————————02大类权限————————

# ————————04大类权限————————
# 040103_学生自己的上课记录_GET
def own_studyrecords(request, *args, **kwargs):
    url_path = request.path  # 获取URL 路径 /bpm/studyrecords/6/
    url_list = re.findall( '(\w+)', url_path )  # 正者表达式 获取参数
    url_model_name = url_list[1]
    url_parameter = int( url_list[2] )
    model_name = 'studyrecords'
    if url_model_name == model_name:  # 防止其他表通过权限
        if request.user.id:  # 如果有ID
            list = request.user.stu_account.enrollment_set.all()  # 根据ID关联学生的报名ID
            list_id = []
            for obtain in list:
                results = obtain.id
                list_id.append( results )  # 生成列表
        if url_parameter in list_id:  # 对比URL参数 在不在 ID列表里
            return True
        else:
            return False
    else:
        return False


# 040105_学生自己的作业详情_GET
def own_homework_detail(request, *args, **kwargs):
    url_path = request.path  # 获取URL 路径 /bpm/homework_detail/2/25/
    url_list = re.findall( '(\w+)', url_path )  # 正者表达式 获取参数
    url_model_name = url_list[1]  #字符串
    url_parameter =(int(url_list[2]),)  #元组
    url_parameter2 = int(url_list[3]),  #元组
    model_name = 'homework_detail'#字符串
    if url_model_name == model_name: #防止其他表通过权限
        if request.user.id:  # 如果有ID
            list_id = request.user.stu_account.enrollment_set.values_list('id')  # 根据登陆ID关联学生的报名ID
        if url_parameter in list_id:  # 对比URL参数 在不在 ID列表里
            StudyRecord_id = models.StudyRecord.objects.filter(student_id=url_parameter).values_list('id')
            if url_parameter2 in StudyRecord_id: # 对比URL参数2 在不在 ID列表里
                return True
            else:
                return False
        else:
            return False
    else:
        return False

# ————————04大类权限————————

# ————————05大类权限————————
# 050103_讲师查看自己的课节详情_GET
def own_teacher_class_detail(request, *args, **kwargs):
    url_path = request.path  # 获取URL 路径 /bpm/teacher_class_detail/1/
    url_list = re.findall( '(\w+)', url_path )  # 正者表达式 获取参数
    url_model_name = url_list[1]
    url_parameter = (int(url_list[2]),)  # <class 'tuple'> (1,)
    model_name = 'teacher_class_detail'
    if url_model_name == model_name: #防止其他表通过权限
        if request.user.id:  # 如果有ID
            list_id = request.user.classlist_set.values_list('id')  # 根据ID获取班级ID
        if url_parameter in list_id:  # 对比URL参数 在不在 ID列表里
            return True
        else:
            return False
    else:
        return False

# 050105_讲师查看自己的课节学员_GET
def own_teacher_lesson_detail(request, *args, **kwargs):
    url_path = request.path  # 获取URL 路径 /bpm/teacher_lesson_detail/2/2/
    url_list = re.findall( '(\w+)', url_path )  # 正者表达式 获取参数
    url_model_name = url_list[1]        #字符串
    url_parameter = int(url_list[2]),    #元组
    url_parameter2 = (int(url_list[3]),) #元组
    model_name = 'teacher_lesson_detail'#字符串
    if url_model_name == model_name: #防止其他表通过权限
        if request.user.id:  # 如果有ID
            list_id= request.user.classlist_set.values_list( 'id' ) # 元组列表 #根据登陆ID 反查班级ID列表
        if url_parameter in list_id :  # 对比URL参数 在不在 ID列表里
            CourseRecord_id = models.CourseRecord.objects.filter( from_class_id=url_parameter ).values_list( 'id' )# 元组列表
            if url_parameter2 in CourseRecord_id: # 对比URL参数2 在不在 ID列表里
                return True
            else:
                return False
        else:
            return False
    else:
        return False

# 050107_讲师自己的学员作业下载_GET
def own_howk_down(request, *args, **kwargs):
    url_path = request.path  # 获取URL 路径 /bpm/homeworks/3/3/17/
    url_list = re.findall( '(\w+)', url_path )  # 正者表达式 获取参数
    url_model_name = url_list[1] #字符串
    url_parameter = (int(url_list[2]),)  #元组# <class 'tuple'> (1,)
    url_parameter2 = (int(url_list[3]),) #元组
    model_name = 'homeworks' #字符串
    if url_model_name == model_name: #防止其他表通过权限
        if request.user.id:  # 如果有ID
            list_id = request.user.classlist_set.values_list( 'id' ) # 元组列表 #根据登陆ID 反查班级ID列表
        if url_parameter in list_id :  # 对比URL参数 在不在 ID列表里
            CourseRecord_id = models.CourseRecord.objects.filter( from_class_id=url_parameter ).values_list( 'id' )
            if url_parameter2 in CourseRecord_id: # 对比URL参数2 在不在 ID列表里
                return True
            else:
                return False
        else:
            return False
    else:
        return False

# ————————05大类权限————————

# ————————06大类权限————————

# 060101_讲师查看自己的班级排名详情_GET
def JM_crm_classlist_teachers(request, *args, **kwargs):
    url_path = request.path  # 获取URL 路径 /bpm/coursetop_details/3/
    url_list = re.findall( '(\w+)', url_path )  # 正者表达式 获取参数
    url_model_name = (url_list[1],)#字符串元组
    url_parameter = (int(url_list[2]),)  # 元组 #<class 'tuple'> (1,)
    model_name =[('coursetop_details',),('coursetop_score',),('coursetop_homework',),('coursetop_attendance',),]
    if url_model_name in model_name: #防止其他表通过权限
        if request.user.id:  # 如果有ID
            list_id = request.user.classlist_set.values_list('id')  # 根据ID获取班级ID
            print('list_id::',list_id)
        if url_parameter in list_id:  # 对比URL参数 在不在 ID列表里
            return True
        else:
            return False
    else:
        return False

# ————————06大类权限————————

# ————————74PerfectCRM实现CRM权限和权限组限制访问URL————————

# CJ.py