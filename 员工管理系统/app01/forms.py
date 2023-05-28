# -*- coding: utf-8 -*-
# @Author: XuTianDe
# @Date: 2023-05-21 23:01:41

from django import forms
from django.core.exceptions import ValidationError

from app01 import models
from app01.utils.bootstarp import BootStrapModelForm
from app01.utils.encrypt import md5


# 添加用户表单
class UserModelForm(BootStrapModelForm):
    # 表单验证
    name = forms.CharField(min_length=2, max_length=8, label='用户名')

    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'account', 'create_time', 'gender', 'depart']

        # widgets={     繁琐
        #     'name':forms.TextInput(attrs={"class":"form-control"}),
        #     'password': forms.PasswordInput(attrs={"class": "form-control"}),
        #
        # }

    # # 简洁样式
    # def __init__(self, *args, **kwargs):
    #     # super父类，重新定义__init__方法
    #     super().__init__(*args, **kwargs)
    #
    #     # 获取定义的每个字段
    #     # 循环给每个字段加入类名class：form-control
    #     for name, field in self.fields.items():
    #         # print(name,field)
    #         field.widget.attrs = {'class': 'form-control', "placeholder": field.label}


from django.core.validators import RegexValidator


# 添加靓号表单
class PrettyModelForm(forms.ModelForm):
    # price=forms.CharField(disabled=True,label='价格')   价格不可改
    mobile = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式有误!')]
    )

    class Meta:
        model = models.PrettyNum
        # fields=['mobile','price','level','status']
        # exclude=['level'] 排除什么字段
        fields = '__all__'  # 表示全部字段

    # 简化
    def __init__(self, *args, **kwargs):
        # super父类，重新定义__init__方法
        super().__init__(*args, **kwargs)

        # 获取定义的每个字段
        # 循环给每个字段加入类名class：form-control
        for name, field in self.fields.items():
            # print(name,field)
            field.widget.attrs = {'class': 'form-control', "placeholder": field.label, }

    # 钩子函数判断手机号是否存在
    # def clean_mobile(self):
    #     # 当前编辑的ID，pk=primary_key  主键
    #     print(self.instance.pk)
    #     txt_mobile = self.cleaned_data['mobile']
    #     exits = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
    #
    #     if exits:
    #         raise ValidationError('手机号码已存在!')
    #     return txt_mobile


# 添加靓号表单
class PrettyEditModelForm(BootStrapModelForm):
    # price=forms.CharField(disabled=True,label='价格')   价格不可改
    mobile = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式有误!')]
    )

    class Meta:
        model = models.PrettyNum
        # fields=['mobile','price','level','status']
        # exclude=['level'] 排除什么字段
        fields = '__all__'  # 表示全部字段

    # # 简洁
    # def __init__(self, *args, **kwargs):
    #     # super父类，重新定义__init__方法
    #     super().__init__(*args, **kwargs)
    #
    #     # 获取定义的每个字段
    #     # 循环给每个字段加入类名class：form-control
    #     for name, field in self.fields.items():
    #         # print(name,field)
    #         field.widget.attrs = {'class': 'form-control', "placeholder": field.label}

    # 钩子函数判断手机号是否存在
    def clean_mobile(self):
        # 当前编辑的ID，pk=primary_key  主键
        now_id = self.instance.pk
        txt_mobile = self.cleaned_data['mobile']
        # exclude为排除这个id，后面接着是查找除了这个id以外的所有手机号
        exits = models.PrettyNum.objects.exclude(id=now_id).filter(mobile=txt_mobile).exists()
        if exits:
            raise ValidationError('手机号码已存在!')
        return txt_mobile


# 添加管理员验证
class AdminModelForm(BootStrapModelForm):
    widget = forms.PasswordInput  # 文本框变密码框
    # password = forms.CharField(label='密码', max_length=18, widget=widget)
    confirm_password = forms.CharField(label='确认密码', max_length=18, widget=widget)

    class Meta:
        model = models.Admin
        fields = ['username', 'password', 'confirm_password']
        widgets = {
            "password": forms.PasswordInput,
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        md5_pw = md5(password)
        print(self.instance.pk)  # 获取当前对象的id
        return md5_pw

    # 判断两次输入的密码是否正确
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = md5(self.cleaned_data.get("confirm_password"))

        if confirm_password != password:
            raise ValidationError("密码不一致")
        # 返回什么，保存到数据库的就是什么
        return confirm_password


# 管理员编辑的表单
class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']

        widgets = {
            "password": forms.PasswordInput,
        }


# 重置密码的表单
class AdminResetModelForm(BootStrapModelForm):
    widget = forms.PasswordInput  # 文本框变密码框
    # password = forms.CharField(label='密码', max_length=18, widget=widget)
    confirm_password = forms.CharField(label='确认密码', max_length=18, widget=widget)

    class Meta:
        model = models.Admin
        fields = ['password', 'confirm_password']
        widgets = {
            "password": forms.PasswordInput,
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        md5_pw = md5(password)
        # print(self.instance.pk)  # 获取当前对象的id
        # 判断输入的密码与数据库中的密码是否一致
        extis=models.Admin.objects.filter(id=self.instance.pk,password=md5_pw).exists()
        # 存在则提示
        if extis:
            raise ValidationError("不能与原密码保持一致!")
        return md5_pw
