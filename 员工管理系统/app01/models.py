from django.db import models


class Registration(models.Model):
    """注册"""


class Login(models.Model):
    """登录"""
    username = models.CharField(verbose_name='用户名', max_length=11)
    password = models.CharField(verbose_name='密码', max_length=18)


class Admin(models.Model):
    """管理员表"""
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)

    def __str__(self):
        return self.username


class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name='标题', max_length=32)  # verbose_name注解

    # 魔术方法
    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name='姓名', max_length=16)
    password = models.CharField(verbose_name='密码', max_length=32)
    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(verbose_name='账户余额', max_digits=10, decimal_places=2,
                                  default=0)  # 最大长度为10，小数点长度为2，新创建用户余额为0
    create_time = models.DateField(verbose_name='入职时间')

    # 无约束
    # depart_id=models.BigIntegerField(verbose_name='部门ID')

    # 1.有约束
    #     to ，与那张表关联
    #     to_field 表中哪一列关联
    # 2.django自动
    #     写的是depart变量名，生成数据列的时候是depart_id
    # 3.部门表被删除
    #     3.1on_delete = models.CASCADE级联删除
    depart = models.ForeignKey(verbose_name='部门', to='Department', to_field='id', on_delete=models.CASCADE)
    # #     3.2允许为空on_delete=models.SET_NULL,null=True
    # depart=models.ForeignKey(to='Department',to_field='id',on_delete=models.SET_NULL,null=True)

    # Django中的约束
    gender_choices = (
        (0, '男'),
        (1, '女')
    )
    # 创建数据对象的时候0代表男，1代表女
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)


class PrettyNum(models.Model):
    """靓号表"""

    mobile = models.CharField(verbose_name='手机号', max_length=11)
    price = models.IntegerField(verbose_name='价格', default=0)  # 想要允许为空，加上null=True,blank=True
    level_choices = (
        (1, '一级'),
        (2, '二级'),
        (3, '三级'),
        (4, '四级'),

    )
    level = models.SmallIntegerField(verbose_name='级别', choices=level_choices, default=1)  # SmallIntegerField小整形
    status_choices = (
        (1, '已占用'),
        (2, '未使用')
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices, default=2)


class Task(models.Model):
    """任务表"""
    level_choices = (
        (1, "紧急"),
        (2, "重要"),
        (3, "一般"),

    )
    level = models.SmallIntegerField(verbose_name='级别', choices=level_choices, default=1)

    title = models.CharField(verbose_name='标题', max_length=64)
    detail = models.TextField(verbose_name='详细信息')
    user = models.ForeignKey(verbose_name='管理员', to='Admin', on_delete=models.CASCADE)


# AJAX实现
class Order(models.Model):
    """订单"""
    oid = models.CharField(verbose_name='订单号', max_length=64)
    title = models.CharField(verbose_name='名称', max_length=64)
    price = models.IntegerField(verbose_name='价格')
    status_choices = (
        (1, "待支付"),
        (2, "已支付"),

    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices, default=1)
    admin = models.ForeignKey(verbose_name='用户', to=Admin, on_delete=models.CASCADE)  # 级别，管理表删除了跟着删除


# 文件上传的表
# form上传的表单
class Boss(models.Model):
    """文件表"""
    name = models.CharField(verbose_name='姓名', max_length=32)
    age = models.IntegerField(verbose_name='年龄')
    img = models.CharField(verbose_name='头像', max_length=320)

# modelform上传的表
class City(models.Model):
    """文件表"""
    name = models.CharField(verbose_name='城市', max_length=32)
    count = models.IntegerField(verbose_name='人口')
    # FileField与CharField两者本质上相同，在数据中都是CharField，FileField可以自动保存数据，upload_to=...
    img = models.FileField(verbose_name='Logo', max_length=320,upload_to='city/')
