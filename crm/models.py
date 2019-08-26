from django.db import models
# Create your models here.
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.utils.translation import ugettext_lazy as _  # 语言国际化
from django.utils.safestring import mark_safe

"""01校区表"""
class Branch(models.Model):
    name = models.CharField(max_length=128,unique=True) #校区名#CharField作用是保存文本，定长的变量类型
    addr = models.CharField(max_length=128) #地址
    def __str__(self):#__str__()是Python的一个“魔幻”方法，这个方法定义了当object调用str()时应该返回的值。
        return self.name #返回 #校区名
    class Meta: #通过一个内嵌类 "class Meta" 给你的 model 定义元数据
        verbose_name_plural =  "01校区表" #verbose_name_plural给你的模型类起一个更可读的名字

"""02班级表"""
class ClassList(models.Model):
    #ForeignKey就是表与表之间的某种约定的关系  #CASCADE从父表删除或更新且自动删除或更新子表中匹配的行。
    branch = models.ForeignKey("Branch",on_delete=models.CASCADE)#校区    关联到  校区表
    course = models.ForeignKey("Course",on_delete=models.CASCADE) #课程   关联到   课程表

    contract = models.ForeignKey('ContractTemplate', blank=True, null=True, default=1,on_delete=models.CASCADE)  # 合同表

    class_type_choices = ( #上课形式
                          (0,'面授(脱产)'),
                          (1,'面授(周末)'),
                          (2,'网络班'),)
    #PositiveSmallIntegerField正小整数 0 ～ 32767 #choices是Admin中显示选择框的内容，用不变动的数据放在内存中从而避免跨表操作
    class_type = models.SmallIntegerField(choices=class_type_choices)#上课形式

    #PositiveSmallIntegerField正小整数 0 ～ 32767
    semester = models.PositiveSmallIntegerField(verbose_name="学期") #课程的第几期

    #ManyToManyField多对多和外键工作方式相同，只不过我们处理的是QuerySet而不是模型实例。
    teachers = models.ManyToManyField("UserProfile") # 老师   关联到    账号表

    start_date = models.DateField(verbose_name="开班日期") #DateField 日期格式 YYYY-MM-DD #verbose_name是Admin中显示的字段名称

    # DateField 日期格式 YYYY-MM-DD #verbose_name是Admin中显示的字段名称 #Django可空#数据库可以为空
    end_date = models.DateField(verbose_name="结业日期",blank=True,null=True)

    def __str__(self):
        try:
            return "%s %s %s" %(self.branch,self.course,self.semester) #返回 #%s格式化输出字符串 #校区#课程# 学期
        except:
            return "添加班级表"
    
    class Meta:#通过一个内嵌类 "class Meta" 给你的 model 定义元数据
        unique_together=('branch','course','semester')  #联合索引
        verbose_name_plural = "02班级表" #verbose_name_plural给你的模型类起一个更可读的名字

"""03课程表，可以报名那些课程"""
class Course(models.Model):
    name = models.CharField(max_length=64,unique=True)#课程名 #CharField作用是保存文本，定长的变量类型
    price = models.PositiveSmallIntegerField(verbose_name="学费")#学费#PositiveSmallIntegerField正小整数 0 ～ 32767
    period = models.PositiveSmallIntegerField(verbose_name="周期（月）") #PositiveSmallIntegerField正小整数 0 ～ 32767
    outline = models.TextField() #课程大纲  #文本类型
    def __str__(self):#__str__()是Python的一个“魔幻”方法，这个方法定义了当object调用str()时应该返回的值。
        return self.name #返回 #课程名
    class Meta:#通过一个内嵌类 "class Meta" 给你的 model 定义元数据
        verbose_name_plural =  "03课程表"#verbose_name_plural给你的模型类起一个更可读的名字

'''04客户信息表'''
class Customer(models.Model):
    name = models.CharField(max_length=32,blank=True,null=True)#客户名#CharField定长文本 #名字最长32 # Django可空 #数据库可以为空
    qq = models.CharField(max_length=64,unique=True) #QQ号#CharField定长文本 #名字最长64 #唯一，不能重复
    qq_name = models.CharField(max_length=64,blank=True,null=True)#QQ名 #CharField定长文本 #名字最长64 # Django可空 #数据库可以为空
    phone = models.CharField(max_length=64,blank=True,null=True)#手机号 #CharField定长文本 #名字最长64 # Django可空 #数据库可以为空

    id_num=models.CharField(max_length=64,blank=True,null=True,verbose_name='身份证号')#身份证号
    email=models.EmailField(max_length=64,blank=True,null=True,verbose_name='邮箱')#email
    sex_choices=((0,'保密'),(1,'男'),(2,'女'))
    sex=models.SmallIntegerField(choices=sex_choices,default=0,verbose_name='性别')

    status_choices = ((0, '已报名'), (1, '未报名'), (2, '已退学'))
    status = models.SmallIntegerField(choices=status_choices, default=1)  # 学员状态

    source_choices = ( #客户渠道来源 （内存生成）
                      (0,'转介绍'),
                      (1,'QQ群'),
                      (2,'官网'),
                      (3,'百度推广'),
                      (4,'51CTO'),
                      (5,'知乎'),
                      (6,'市场推广'),)
    #PositiveSmallIntegerField正小整数 0 ～ 32767（省空间）#choices是Admin中显示选择框的内容，用不变动的数据放在内存中从而避免跨表操作
    source = models.SmallIntegerField(choices=source_choices)#客户渠道来源

    #CharField定长文本#verbose_name是Admin中显示的字段名称#名字最长64 # Django可空 #数据库可以为空
    referral_from = models.CharField(verbose_name="转介绍人qq",max_length=64,blank=True,null=True) #来自谁介绍的

    #ForeignKey就是表与表之间的某种约定的关系#verbose_name是Admin中显示的字段名称 #CASCADE从父表删除或更新且自动删除或更新子表中匹配的行。
    consult_courses = models.ForeignKey("Course",verbose_name="咨询课程", on_delete=models.CASCADE) #关联到 课程表

    content= models.TextField(verbose_name="咨询详情") #TextField无限制长度的文本#verbose_name是Admin中显示的字段名称

    #ManyToManyField多对多和外键工作方式相同，只不过我们处理的是QuerySet而不是模型实例。
    tags = models.ManyToManyField("Tag",blank=True)#多对多关联到 标签表

    #ForeignKey就是表与表之间的某种约定的关系  #CASCADE从父表删除或更新且自动删除或更新子表中匹配的行。
    consultant = models.ForeignKey("UserProfile", on_delete=models.CASCADE) #关联到  账号表

    memo = models.TextField(blank=True,null=True)#备注#TextField无限制长度的文本#Django可空#数据库可以为空

    #DateTimeField日期+时间格式 YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] #auto_now_add创建时间（只读）
    date =  models.DateTimeField(auto_now_add=True)#创建时间（数据库自增）

    def __str__(self): #__str__()是Python的一个“魔幻”方法，这个方法定义了当object调用str()时应该返回的值。
        return self.qq  #返回 #QQ号

    class Meta:#通过一个内嵌类 "class Meta" 给你的 model 定义元数据
        verbose_name_plural =  "04客户表" #verbose_name_plural给你的模型类起一个更可读的名字

#合同模版
class ContractTemplate(models.Model):
    name=models.CharField('合同名称',max_length=64,unique=True)
    template=models.TextField()

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural='合同表'

"""05客户跟进表"""
class CustomerFollowUp(models.Model):

    #ForeignKey就是表与表之间的某种约定的关系 #CASCADE从父表删除或更新且自动删除或更新子表中匹配的行。
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)#客户名 #关联到  客户信息表

    content = models.TextField(verbose_name="跟进内容")#跟进的内容#TextField无限制长度的文本#verbose_name是Admin中显示的字段名称

    #ForeignKey就是表与表之间的某种约定的关系  #CASCADE从父表删除或更新且自动删除或更新子表中匹配的行。
    consultant =models.ForeignKey("UserProfile", on_delete=models.CASCADE) #关联到  账号表

    intention_choices =(  #报名状态
                        (0,'2周内报名'),
                        (1,'1个月内报名'),
                        (2,'近期无报名计划'),
                        (3,'已在其它机构报名'),
                        (4,'已报名'),
                        (5,'已拉黑'),)
    #PositiveSmallIntegerField正小整数 0 ～ 32767（省空间）#choices是Admin中显示选择框的内容，用不变动的数据放在内存中从而避免跨表操作
    intention=models.SmallIntegerField(choices=intention_choices) #报名状态

    #DateTimeField日期+时间格式 YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] #auto_now_add创建时间（只读）
    date =  models.DateTimeField(auto_now_add=True)#创建时间（数据库自增）

    def __str__(self):#__str__()是Python的一个“魔幻”方法，这个方法定义了当object调用str()时应该返回的值。
        return "<%s:%s>" %(self.customer.qq,self.intention) #返回#格式化字符串#跨表里的QQ号#报名状态
    class Meta:#通过一个内嵌类 "class Meta" 给你的 model 定义元数据
        verbose_name_plural =  "05客户跟进表"#verbose_name_plural给你的模型类起一个更可读的名字

"""06学员报名信息表"""
class Enrollment(models.Model):
    # ForeignKey就是表与表之间的某种约定的关系#verbose_name是Admin中显示的字段名称 #CASCADE从父表删除或更新且自动删除或更新子表中匹配的行。
    customer = models.ForeignKey("Customer",on_delete=models.CASCADE)#学员名字 #关联到  客户信息表
    enrolled_class = models.ForeignKey("ClassList",verbose_name="所报班级",on_delete=models.CASCADE)#关联到  班级表
    consultant = models.ForeignKey("UserProfile",verbose_name="课程顾问",on_delete=models.CASCADE) #关联到  账号表

    contract_review = models.CharField(max_length=256, blank=True, null=True, verbose_name='合同审核')
    #BooleanField布尔值类型#default=False默认(True)不允许出现空字符#verbose_name是Admin中显示的字段名称
    contract_agreed = models.BooleanField(default=False,verbose_name="学员已经同意合同")#学员看合同
    contract_approved = models.BooleanField(default=False,verbose_name="合同已经审核") #谁审核
    
    Pay_cost= models.BooleanField(default=False,verbose_name="缴费") #缴费状态#是不是交定金
    # DateTimeField日期+时间格式 YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] #auto_now_add创建时间（只读）
    date = models.DateTimeField(auto_now_add=True)#创建时间（数据库自增）

    def __str__(self):#__str__()是Python的一个“魔幻”方法，这个方法定义了当object调用str()时应该返回的值。
        return "%s %s" %(self.customer,self.enrolled_class)#返回#格式化字符串#学员名字#所报班级
        
    class Meta:#通过一个内嵌类 "class Meta" 给你的 model 定义元数据
        unique_together =  ("customer","enrolled_class")#联合索引
        verbose_name_plural =  "06学员报名信息表"#verbose_name_plural给你的模型类起一个更可读的名字

"""07缴费记录表"""
class Payment(models.Model):
    #ForeignKey就是表与表之间的某种约定的关系#verbose_name是Admin中显示的字段名称 #CASCADE从父表删除或更新且自动删除或更新子表中匹配的行。
    customer = models.ForeignKey("Customer",on_delete=models.CASCADE)#学员名字        关联到  客户信息表
    course = models.ForeignKey("Course",verbose_name="所报课程",on_delete=models.CASCADE)#关联到  课程表

    #PositiveSmallIntegerField正小整数 0 ～ 32767 #verbose_name是Admin中显示的字段名称#默认值=500
    amount = models.PositiveIntegerField(verbose_name="数额",default=500)#缴费数额

    #ForeignKey就是表与表之间的某种约定的关系#CASCADE从父表删除或更新且自动删除或更新子表中匹配的行。
    consultant = models.ForeignKey("UserProfile",on_delete=models.CASCADE)#缴费给谁 关联到  账号表

    #DateTimeField日期+时间格式 YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] #auto_now_add创建时间（只读）
    date=models.DateTimeField(auto_now_add=True)#创建时间（数据库自增）

    def __str__(self):#__str__()是Python的一个“魔幻”方法，这个方法定义了当object调用str()时应该返回的值。
        return "%s %s" %(self.customer,self.amount)#返回#格式化字符串#学员名字#缴费数额
    class Meta:#通过一个内嵌类 "class Meta" 给你的 model 定义元数据
        verbose_name_plural = "07缴费记录表"#verbose_name_plural给你的模型类起一个更可读的名字

"""08每节课上课纪录表"""
class CourseRecord(models.Model):
    from_class = models.ForeignKey("ClassList",verbose_name="班级",on_delete=models.CASCADE) #那个班级

    day_num = models.PositiveSmallIntegerField(verbose_name="第几节(天)") #第几节课
    teacher = models.ForeignKey("UserProfile",on_delete=models.CASCADE)#老师是谁    关联到    账号表
    has_homework = models.BooleanField(default=True) #有没有作业
    homework_title = models.CharField(max_length=128,blank=True,null=True) #作业标题
    homework_content = models.TextField(blank=True,null=True) #作业内容
    outline =models.TextField(verbose_name="本节课程大纲") #课程主要讲什么
    date = models.DateField(auto_now_add=True)#创建时间（数据库自增）

    def __str__(self):
        try:
            return " %s:%s" %(self.from_class,self.day_num)#返回#格式化字符串#班级#第几节(天)
        except:
            return "添加上课纪录"
        
    class Meta:#通过一个内嵌类 "class Meta" 给你的 model 定义元数据
        unique_together = ("from_class","day_num") #联合索引
        verbose_name_plural = "08每节课上课纪录表" #verbose_name_plural给你的模型类起一个更可读的名字

"""09学习纪录"""
class StudyRecord(models.Model):
    student = models.ForeignKey("Enrollment",on_delete=models.CASCADE)#学生名字   关联到    学员报名信息表
    course_record = models.ForeignKey("CourseRecord",on_delete=models.CASCADE)#开课记录   # 关联到    每节课上课纪录表

    attendance_choices = (# 本节课上课状态记录
                            (0,"已签到"),
                            (1,"迟到"),
                            (2,"缺勤"),
                            (3,"早退"),)
    #PositiveSmallIntegerField正小整数 0 ～ 32767（省空间）#choices是Admin中显示选择框的内容，用不变动的数据放在内存中从而避免跨表操作
    attendance = models.SmallIntegerField(choices=attendance_choices) # 本节课上课状态记录
    delivery = models.BooleanField(default=False,verbose_name="交作业") #有没有交付作业
    homework_link = models.TextField(blank=True, null=True)

    score_choices = (#学习成绩
                     (100,"A+"),
                     (90,"A"),
                     (85,"B+"),
                     (80,"B"),
                     (75,"B-"),
                     (70,"C+"),
                     (65,"C"),
                     (40,"C-"),
                     (-20,"D"),
                     (-50,"COPY"),
                     (0,"N/A"),)
    #PositiveSmallIntegerField正小整数 0 ～ 32767（省空间）#choices是Admin中显示选择框的内容，用不变动的数据放在内存中从而避免跨表操作
    score = models.SmallIntegerField(choices=score_choices) #学习成绩

    memo = models.TextField(blank=True,null=True)#TextField无限制长度的文本#Django可空#数据库可以为空

    # DateTimeField日期+时间格式 YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] #auto_now_add创建时间（只读）
    date = models.DateField(auto_now_add=True)#创建时间（数据库自增）

    def __str__(self):#__str__()是Python的一个“魔幻”方法，这个方法定义了当object调用str()时应该返回的值。
        return "%s %s %s" % (self.student, self.course_record, self.score)#返回#格式化字符串#学生名字#开课记录#学习成绩
    class Meta:#通过一个内嵌类 "class Meta" 给你的 model 定义元数据
        unique_together = ('student','course_record')#联合索引#学生名字#开课记录
        verbose_name_plural =  "09学习纪录"#verbose_name_plural给你的模型类起一个更可读的名字

"""10账号表"""
"""
class UserProfile(models.Model):
    from django.contrib.auth.models import User  # 使用django内置的用户表

    #OneToOneField一对一  #User是django Admin里的账号表#CASCADE从父表删除或更新且自动删除或更新子表中匹配的行。
    user = models.OneToOneField(User,on_delete=models.CASCADE)# 用户名 #创建外键，关联django用户表

    name = models.CharField(max_length=32) #账号名（扩展用户字段）#CharField定长文本

    #ManyToManyField多对多和外键工作方式相同，只不过我们处理的是QuerySet而不是模型实例。#Django可空
    roles = models.ManyToManyField("Role",blank=True) #角色(权限)   # 双向一对多==多对多

    def __str__(self):
        return self.name #返回 #账号名
    class Meta: #通过一个内嵌类 "class Meta" 给你的 model 定义元数据
        verbose_name_plural = "10账号表"#verbose_name_plural给你的模型类起一个更可读的名字
"""

class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
    　　创建并保存一个用户用给定的邮件,日期
    　　出生和密码。
        """
        if not email:#没有email 报错
            raise ValueError('用户必须有一个电子邮件地址')

        user = self.model(
            email=self.normalize_email(email),#验证邮箱格式
            name=name,
        )
        user.set_password(password)#加密
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
    　　创建并保存一个超级用户具有给定邮件,日期
    　　出生和密码。
        """
        user = self.create_user(email,
            password=password,
            name=name
        )
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    email=models.EmailField(
        verbose_name='邮箱账号',
        max_length=255,
        unique=True#唯一  #登陆账号
    )
    name=models.CharField(max_length=32,verbose_name='用户名')
    password = models.CharField(_('password'), max_length=128, help_text=mark_safe('''<a href=\"../password/\">修改密码</a>'''))

    is_active = models.BooleanField(default=True,verbose_name='合法账号')#权限#合法账号
    is_superuser = models.BooleanField(default=False,verbose_name='超级账号') #超级账号
    USERNAME_FIELD ='email'#指定做为  #登陆账号
    REQUIRED_FIELDS = ['name']#必填字段

    branch = models.ForeignKey( "Branch", verbose_name="所属校区", blank=True, null=True, on_delete=models.CASCADE )
    roles = models.ManyToManyField( 'Role', verbose_name="角色", blank=True )
    memo = models.TextField( blank=True, null=True, default=None, verbose_name="备注" )
    from django.utils import timezone
    date_joined = models.DateTimeField( verbose_name="创建时间", default=timezone.now )
    
    stu_account=models.ForeignKey("Customer",verbose_name='关联学员帐号',blank=True,null=True,on_delete=models.CASCADE,help_text='报名成功后创建关联帐户')

    objects = UserProfileManager()#创建账号 #关联这个函数

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        #用户确认的电子邮件地址
        return self.email

    def __str__(self):
        return self.name

    def has_perm(self,perm,obj=None):
        #指明用户是否被认为活跃的。以反选代替删除帐号。
        #最简单的可能的答案:是的,总是
        return True   #有效 账号

    def has_module_perms(self, app_label):
        #指明用户是否可以登录到这个管理站点。
        # 最简单的可能的答案:是的,总是
        return True #职员状态

    class Meta: #通过一个内嵌类 "class Meta" 给你的 model 定义元数据
        verbose_name_plural = "0用户"
    @property
    def is_staff(self):
        '''“用户的员工吗?”'''
        #最简单的可能的答案:所有管理员都是员工
        return self.is_superuser#是不是超级用户状态

    class Meta:
        verbose_name_plural = '10CRM账户表'
        permissions = (
            ('crm_010101_all_table_data_list_GET', '010101_全部查看数据_GET'),
            ('crm_010102_all_table_data_list_POST', '010102_全部查看数据_POST'),
            ('crm_010103_all_table_add_GET', '010103_全部添加数据_GET'),
            ('crm_010104_all_table_add_POST', '010104_全部添加数据_POST'),
            ('crm_010105_all_table_change_GET', '010105_全部修改数据_GET'),
            ('crm_010106_all_table_change_POST', '010106_全部修改数据_POST'),
            ('crm_010107_all_table_delete_GET', '010107_全部删除数据_GET'),
            ('crm_010108_all_table_delete_POST', '010108_全部删除数据_POST'),
            ('crm_010109_all_password_reset_GET', '010109_全部密码重置_GET'),
            ('crm_010110_all_password_reset_POST', '010110_全部密码重置_POST'),

            ('crm_010201_only_view_Branch_GET', '010201_只能查看校区表_GET'),
            ('crm_010202_only_view_Branch_POST', '010202_只能查看校区表_POST'),
            ('crm_010203_only_add_Branch_GET', '010203_只能添加校区表_GET'),
            ('crm_010204_only_add_Branch_POST', '010204_只能添加校区表_POST'),
            ('crm_010205_only_change_Branch_GET', '010205_只能修改校区表_GET'),
            ('crm_010206_only_change_Branch_POST', '010206_只能修改校区表_POST'),
            ('crm_010207_only_delete_Branch_GET', '010207_只能删除校区表_GET'),
            ('crm_010208_only_delete_Branch_POST', '010208_只能删除校区表_POST'),

            ('crm_010301_only_view_ClassList_GET', '010301_只能查看班级表_GET'),
            ('crm_010302_only_view_ClassList_POST', '010302_只能查看班级表_POST'),
            ('crm_010303_only_add_ClassList_GET', '010303_只能添加班级表_GET'),
            ('crm_010304_only_add_ClassList_POST', '010304_只能添加班级表_POST'),
            ('crm_010305_only_change_ClassList_GET', '010305_只能修改班级表_GET'),
            ('crm_010306_only_change_ClassList_POST', '010306_只能修改班级表_POST'),
            ('crm_010307_only_delete_ClassList_GET', '010307_只能删除班级表_GET'),
            ('crm_010308_only_delete_ClassList_POST', '010308_只能删除班级表_POST'),

            ('crm_010401_only_view_Course_GET', '010401_只能查看课程表_GET'),
            ('crm_010402_only_view_Course_POST', '010402_只能查看课程表_POST'),
            ('crm_010403_only_add_Course_GET', '010403_只能添加课程表_GET'),
            ('crm_010404_only_add_Course_POST', '010404_只能添加课程表_POST'),
            ('crm_010405_only_change_Course_GET', '010405_只能修改课程表_GET'),
            ('crm_010406_only_change_Course_POST', '010406_只能修改课程表_POST'),
            ('crm_010407_only_delete_Course_GET', '010407_只能删除课程表_GET'),
            ('crm_010408_only_delete_Course_POST', '010408_只能删除课程表_POST'),

            ('crm_010501_only_view_Customer_GET', '010501_只能查看客户表_GET'),
            ('crm_010502_only_view_Customer_POST', '010502_只能查看客户表_POST'),
            ('crm_010503_only_add_Customer_GET', '010503_只能添加客户表_GET'),
            ('crm_010504_only_add_Customer_POST', '010504_只能添加客户表_POST'),
            ('crm_010505_only_change_Customer_GET', '010505_只能修改客户表_GET'),
            ('crm_010506_only_change_Customer_POST', '010506_只能修改客户表_POST'),
            ('crm_010507_only_delete_Customer_GET', '010507_只能删除客户表_GET'),
            ('crm_010508_only_delete_Customer_POST', '010508_只能删除客户表_POST'),

            ('crm_010601_only_view_CustomerFollowUp_GET', '010601_只能查看跟进表_GET'),
            ('crm_010602_only_view_CustomerFollowUp_POST', '010602_只能查看跟进表_POST'),
            ('crm_010603_only_add_CustomerFollowUp_GET', '010603_只能添加跟进表_GET'),
            ('crm_010604_only_add_CustomerFollowUp_POST', '010604_只能添加跟进表_POST'),
            ('crm_010605_only_change_CustomerFollowUp_GET', '010605_只能修改跟进表_GET'),
            ('crm_010606_only_change_CustomerFollowUp_POST', '010606_只能修改跟进表_POST'),
            ('crm_010607_only_delete_CustomerFollowUp_GET', '010607_只能删除跟进表_GET'),
            ('crm_010608_only_delete_CustomerFollowUp_POST', '010608_只能删除跟进表_POST'),

            ('crm_010701_only_view_Enrollment_GET', '010701_只能查看报名表_GET'),
            ('crm_010702_only_view_Enrollment_POST', '010702_只能查看报名表_POST'),
            ('crm_010703_only_add_Enrollment_GET', '010703_只能添加报名表_GET'),
            ('crm_010704_only_add_Enrollment_POST', '010704_只能添加报名表_POST'),
            ('crm_010705_only_change_Enrollment_GET', '010705_只能修改报名表_GET'),
            ('crm_010706_only_change_Enrollment_POST', '010706_只能修改报名表_POST'),
            ('crm_010707_only_delete_Enrollment_GET', '010707_只能删除报名表_GET'),
            ('crm_010708_only_delete_Enrollment_POST', '010708_只能删除报名表_POST'),

            ('crm_010801_only_view_Payment_GET', '010801_只能查看缴费表_GET'),
            ('crm_010802_only_view_Payment_POST', '010802_只能查看缴费表_POST'),
            ('crm_010803_only_add_Payment_GET', '010803_只能添加缴费表_GET'),
            ('crm_010804_only_add_Payment_POST', '010804_只能添加缴费表_POST'),
            ('crm_010805_only_change_Payment_GET', '010805_只能修改缴费表_GET'),
            ('crm_010806_only_change_Payment_POST', '010806_只能修改缴费表_POST'),
            ('crm_010807_only_delete_Payment_GET', '010807_只能删除缴费表_GET'),
            ('crm_010808_only_delete_Payment_POST', '010808_只能删除缴费表_POST'),

            ('crm_010901_only_view_CourseRecord_GET', '010901_只能查看上课表_GET'),
            ('crm_010902_only_view_CourseRecord_POST', '010902_只能查看上课表_POST'),
            ('crm_010903_only_add_CourseRecord_GET', '010903_只能添加上课表_GET'),
            ('crm_010904_only_add_CourseRecord_POST', '010904_只能添加上课表_POST'),
            ('crm_010905_only_change_CourseRecord_GET', '010905_只能修改上课表_GET'),
            ('crm_010906_only_change_CourseRecord_POST', '010906_只能修改上课表_POST'),
            ('crm_010907_only_delete_CourseRecord_GET', '010907_只能删除上课表_GET'),
            ('crm_010908_only_delete_CourseRecord_POST', '010908_只能删除上课表_POST'),

            ('crm_011001_only_view_StudyRecord_GET', '011001_只能查看学习表_GET'),
            ('crm_011002_only_view_StudyRecord_POST', '011002_只能查看学习表_POST'),
            ('crm_011003_only_add_StudyRecord_GET', '011003_只能添加学习表_GET'),
            ('crm_011004_only_add_StudyRecord_POST', '011004_只能添加学习表_POST'),
            ('crm_011005_only_change_StudyRecord_GET', '011005_只能修改学习表_GET'),
            ('crm_011006_only_change_StudyRecord_POST', '011006_只能修改学习表_POST'),
            ('crm_011007_only_delete_StudyRecord_GET', '011007_只能删除学习表_GET'),
            ('crm_011008_only_delete_StudyRecord_POST', '011008_只能删除学习表_POST'),

            ('crm_011101_only_view_UserProfile_GET', '011101_只能查看账号表_GET'),
            ('crm_011102_only_view_UserProfile_POST', '011102_只能查看账号表_POST'),
            ('crm_011103_only_add_UserProfile_GET', '011103_只能添加账号表_GET'),
            ('crm_011104_only_add_UserProfile_POST', '011104_只能添加账号表_POST'),
            ('crm_011105_only_change_UserProfile_GET', '011105_只能修改账号表_GET'),
            ('crm_011106_only_change_UserProfile_POST', '011106_只能修改账号表_POST'),
            ('crm_011107_only_delete_UserProfile_GET', '011107_只能删除账号表_GET'),
            ('crm_011108_only_delete_UserProfile_POST', '011108_只能删除账号表_POST'),

            ('crm_011201_only_view_Role_GET', '011201_只能查看角色表_GET'),
            ('crm_011202_only_view_Role_POST', '011202_只能查看角色表_POST'),
            ('crm_011203_only_add_Role_GET', '011203_只能添加角色表_GET'),
            ('crm_011204_only_add_Role_POST', '011204_只能添加角色表_POST'),
            ('crm_011205_only_change_Role_GET', '011205_只能修改角色表_GET'),
            ('crm_011206_only_change_Role_POST', '011206_只能修改角色表_POST'),
            ('crm_011207_only_delete_Role_GET', '011207_只能删除角色表_GET'),
            ('crm_011208_only_delete_Role_POST', '011208_只能删除角色表_POST'),

            ('crm_011301_only_view_Tag_GET', '011301_只能查看标签表_GET'),
            ('crm_011302_only_view_Tag_POST', '011302_只能查看标签表_POST'),
            ('crm_011303_only_add_Tag_GET', '011303_只能添加标签表_GET'),
            ('crm_011304_only_add_Tag_POST', '011304_只能添加标签表_POST'),
            ('crm_011305_only_change_Tag_GET', '011305_只能修改标签表_GET'),
            ('crm_011306_only_change_Tag_POST', '011306_只能修改标签表_POST'),
            ('crm_011307_only_delete_Tag_GET', '011307_只能删除标签表_GET'),
            ('crm_011308_only_delete_Tag_POST', '011308_只能删除标签表_POST'),

            ('crm_011401_only_view_FirstLayerMenu_GET', '011401_只能查看一层菜单_GET'),
            ('crm_011402_only_view_FirstLayerMenu_POST', '011402_只能查看一层菜单_POST'),
            ('crm_011403_only_add_FirstLayerMenu_GET', '011403_只能添加一层菜单_GET'),
            ('crm_011404_only_add_FirstLayerMenu_POST', '011404_只能添加一层菜单_POST'),
            ('crm_011405_only_change_FirstLayerMenu_GET', '011405_只能修改一层菜单_GET'),
            ('crm_011406_only_change_FirstLayerMenu_POST', '011406_只能修改一层菜单_POST'),
            ('crm_011407_only_delete_FirstLayerMenu_GET', '011407_只能删除一层菜单_GET'),
            ('crm_011408_only_delete_FirstLayerMenu_POST', '011408_只能删除一层菜单_POST'),

            ('crm_011501_only_view_SubMenu_GET', '011501_只能查看二层菜单_GET'),
            ('crm_011502_only_view_SubMenu_POST', '011502_只能查看二层菜单_POST'),
            ('crm_011503_only_add_SubMenu_GET', '011503_只能添加二层菜单_GET'),
            ('crm_011504_only_add_SubMenu_POST', '011504_只能添加二层菜单_POST'),
            ('crm_011505_only_change_SubMenu_GET', '011505_只能修改二层菜单_GET'),
            ('crm_011506_only_change_SubMenu_POST', '011506_只能修改二层菜单_POST'),
            ('crm_011507_only_delete_SubMenu_GET', '011507_只能删除二层菜单_GET'),
            ('crm_011508_only_delete_SubMenu_POST', '011508_只能删除二层菜单_POST'),

            ('crm_011601_only_view_Groups_GET', '011601_只能查看权限组_GET'),
            ('crm_011602_only_view_Groups_POST', '011602_只能查看权限组_POST'),
            ('crm_011603_only_add_Groups_GET', '011603_只能添加权限组_GET'),
            ('crm_011604_only_add_Groups_POST', '011604_只能添加权限组_POST'),
            ('crm_011605_only_change_Groups_GET', '011605_只能修改权限组_GET'),
            ('crm_011606_only_change_Groups_POST', '011606_只能修改权限组_POST'),
            ('crm_011607_only_delete_Groups_GET', '011607_只能删除权限组_GET'),
            ('crm_011608_only_delete_Groups_POST', '011608_只能删除权限组_POST'),

            ('crm_011701_own_password_reset_GET', '011701_自己密码重置_GET'),
            ('crm_011702_own_password_reset_POST', '011702_自己密码重置_POST'),

            ('crm_020101_all_not_audit_GET', '020101_销售查看全部的客户未审核_GET'),
            ('crm_020103_all_enrollment_GET', '020103_销售给全部的客户报名课程_GET'),
            ('crm_020104_all_enrollment_POST', '020104_销售给全部的客户报名课程_POST'),
            ('crm_020105_all_contract_review_GET', '020105_销售给全部的客户审核合同_GET'),
            ('crm_020116_all_contract_review_POST', '020116_销售给全部的客户审核合同_POST'),

            ('crm_020201_own_enrollment_GET', '020201_销售给自己的客户报名课程_GET'),
            ('crm_020202_own_enrollment_POST', '020202_销售给自己的客户报名课程_POST'),
            ('crm_020203_own_contract_review_GET', '020203_销售给自己的客户审核合同_GET'),
            ('crm_020204_own_contract_review_POST', '020204_销售给自己的客户审核合同_POST'),

            ('crm_030101_all_not_payment_GET', '030101_财务查看全部的客户未缴费_GET'),
            ('crm_030102_all_not_payment_POST', '030102_财务查看全部的客户未缴费_POST'),
            ('crm_030103_all_already_payment_GET', '030103_财务查看全部的客户已缴费_GET'),
            ('crm_030104_all_already_payment_POST', '030104_财务查看全部的客户已缴费_POST'),
            ('crm_030105_all_payment_GET', '030105_财务进行全部的客户缴费_GET'),
            ('crm_030106_all_payment_POST', '030106_财务进行全部的客户缴费_POST'),

            ('crm_040101_own_student_course_GET', '040101_学生查看自己的课程_GET'),
            ('crm_040102_own_student_course_POST', '040102_学生查看自己的课程_POST'),
            ('crm_040103_own_studyrecords_GET', '040103_学生自己的上课记录_GET'),
            ('crm_040104_own_studyrecords_POST', '040104_学生自己的上课记录_POST'),
            ('crm_040105_own_homework_detail_GET', '040105_学生自己的作业详情_GET'),
            ('crm_040106_own_homework_detail_POST', '040106_学生自己的作业详情_POST'),

            ('crm_050101_own_teacher_class_GET', '050101_讲师查看自己的班级_GET'),
            ('crm_050102_own_teacher_class_POST', '050102_讲师查看自己的班级_POST'),
            ('crm_050103_own_teacher_class_detail_GET', '050103_讲师查看自己的课节详情_GET'),
            ('crm_050104_own_teacher_class_detail_POST', '050104_讲师查看自己的课节详情_POST'),
            ('crm_050105_own_teacher_lesson_detail_GET', '050105_讲师查看自己的课节学员_GET'),
            ('crm_050106_own_teacher_lesson_detail_POST', '050106_讲师查看自己的课节学员_POST'),
            ('crm_050107_own_howk_down_GET', '050107_讲师自己的学员作业下载_GET'),
            ('crm_050108_own_howk_down_POST', '050108_讲师自己的学员作业下载_POST'),

            ('crm_060101_own_coursetop_details_GET', '060101_讲师查看自己的班级排名详情_GET'),
            ('crm_060102_own_coursetop_details_POST', '060102_讲师查看自己的班级排名详情_POST'),
            ('crm_060103_own_coursetop_score_GET', '060103_讲师查看自己的班级分数排行_GET'),
            ('crm_060104_own_coursetop_score_POST', '060104_讲师查看自己的班级排分数排行_POST'),
            ('crm_060105_own_coursetop_homework_GET', '060105_讲师查看自己的班级作业排行_GET'),
            ('crm_060106_own_coursetop_homework_POST', '060106_讲师查看自己的班级作业排行_POST'),
            ('crm_060107_own_coursetop_attendance_GET', '060107_讲师查看自己的班级出勤排行_GET'),
            ('crm_060108_own_coursetop_attendance_POST', '060108_讲师查看自己的班级出勤排行_POST'),

        )


"""11角色表"""
class Role(models.Model):
    name = models.CharField(unique=True,max_length=32)#角色名#CharField定长文本#角色名不可以重复#最长度=32字节
    menus = models.ManyToManyField('FirstLayerMenu',verbose_name='一层菜单',blank=True)

    def __str__(self):#__str__()是Python的一个“魔幻”方法，这个方法定义了当object调用str()时应该返回的值。
        return self.name#返回 #角色名
    
    class Meta: #通过一个内嵌类 "class Meta" 给你的 model 定义元数据
        verbose_name_plural = "11角色表" #verbose_name_plural给你的模型类起一个更可读的名字

"""12标签表"""
class Tag(models.Model):
    name =  models.CharField(max_length=64,unique=True) #标签名#CharField定长文本#最长度=64字节#不可以重复
    def __str__(self): #__str__()是Python的一个“魔幻”方法，这个方法定义了当object调用str()时应该返回的值。
        return self.name #返回 #标签名
    class Meta:#通过一个内嵌类 "class Meta" 给你的 model 定义元数据
        verbose_name_plural =  "12标签表" #verbose_name_plural给你的模型类起一个更可读的名字

"""13一层菜单名"""
class FirstLayerMenu(models.Model):
    '''第一层侧边栏菜单'''
    name = models.CharField('一层菜单名',max_length=64)
    url_type_choices = ((0,'相关的名字'),(1,'固定的URL'))
    url_type = models.SmallIntegerField(choices=url_type_choices,default=0)
    url_name = models.CharField(max_length=64,verbose_name='一层菜单路径')
    order = models.SmallIntegerField(default=0,verbose_name='菜单排序')
    sub_menus = models.ManyToManyField('SubMenu',blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "13第一层菜单"

"""14二层菜单名"""
class SubMenu(models.Model):
    '''第二层侧边栏菜单'''
    name = models.CharField('二层菜单名', max_length=64)
    url_type_choices = ((0,'相关的名字'),(1,'固定的URL'))
    url_type = models.SmallIntegerField(choices=url_type_choices,default=0)
    url_name = models.CharField(max_length=64, verbose_name='二层菜单路径')
    order = models.SmallIntegerField(default=0, verbose_name='菜单排序')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "14第二层菜单"


"""15权限组"""
from django.contrib.auth.models import Group
class Groups(Group):
    class Meta:
        verbose_name_plural = '15权限组'