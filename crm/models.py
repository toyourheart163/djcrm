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

    def __str__(self):#__str__()是Python的一个“魔幻”方法，这个方法定义了当object调用str()时应该返回的值。
        return "%s %s %s" %(self.branch,self.course,self.semester) #返回 #%s格式化输出字符串 #校区#课程# 学期
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
        return " %s:%s" %(self.from_class,self.day_num)#返回#格式化字符串#班级#第几节(天)
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

    @property
    def is_staff(self):
        '''“用户的员工吗?”'''
        #最简单的可能的答案:所有管理员都是员工
        return self.is_superuser#是不是超级用户状态

"""11角色表"""
class Role(models.Model):
    name = models.CharField(unique=True,max_length=32)#角色名#CharField定长文本#角色名不可以重复#最长度=32字节
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
