# -*- coding: utf-8 -*-
# @Author: XuTianDe
# @Date: 2023-05-23 22:58:52
from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, HttpResponse

from app01 import models
from app01.utils.bootstarp import BootStrapModelForm, LoginBootStrapModelForm
from app01.utils.encrypt import md5


# 注册表单
class RegisteredModelForm(LoginBootStrapModelForm):
    widget = forms.PasswordInput  # 文本框变密码框
    # password = forms.CharField(label='密码', max_length=18, widget=widget)
    confirm_password = forms.CharField(label='确认密码', max_length=18, widget=widget)
    code = forms.CharField(label='验证码', max_length=5)

    class Meta:
        model = models.Admin
        fields = ['username', 'password', 'confirm_password', 'code']
        widgets = {
            "password": forms.PasswordInput,
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        md5_pw = md5(password)
        # print(self.instance.pk)  # 获取当前对象的id
        return md5_pw

    # 判断两次输入的密码是否正确
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = md5(self.cleaned_data.get("confirm_password"))

        if confirm_password != password:
            raise ValidationError("密码不一致")
        # 返回什么，保存到数据库的就是什么
        return confirm_password


# 注册功能
def registered(request):
    if request.method == 'GET':
        form = RegisteredModelForm()
        return render(request, 'registered.html', {"form": form})
    form = RegisteredModelForm(data=request.POST)
    if form.is_valid():
        # 先判断该用户是否存在数据库
        username=form.cleaned_data.get('username')
        model=models.Admin.objects.filter(username=username).first()
        if model:
            form.add_error("username","该用户已经存在！")
            return render(request, 'registered.html', {"form": form})

        # print(form.cleaned_data)
        # 不存在则验证验证码是否正确
        # 获取用户的验证码
        user_info_code=form.cleaned_data.pop("code")
        session_code=request.session.get("image_code",'')

        if user_info_code.upper() != session_code.upper():
            form.add_error("code","验证码错误！")
            return render(request, 'registered.html', {"form": form})
        # 验证通过则
        form.save()
        return redirect("/login/")
    return render(request, 'registered.html', {"form": form})
