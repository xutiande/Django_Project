# -*- coding: utf-8 -*-
# @Author: XuTianDe
# @Date: 2023-05-22 11:05:35
from django.shortcuts import render, redirect
from app01.utils.pagination import Pagination
from app01 import models
from app01.forms import PrettyModelForm, PrettyEditModelForm, UserModelForm
from django import forms
from django.http import HttpResponse
from app01.utils.encrypt import md5
from app01.utils.code import check_code
from io import BytesIO

from app01.utils.bootstarp import BootStrapModelForm, LoginBootStrapModelForm


# class LoginForm(forms.Form):
#     username = forms.CharField(label='用户名',
#                                max_length=11,
#                                widget=forms.TextInput)
#     password = forms.CharField(label='密码',
#                                max_length=18,
#                                widget=forms.PasswordInput)
class LoginModelForm(LoginBootStrapModelForm):
    code = forms.CharField(label='验证码', max_length=5)

    class Meta:
        model = models.Admin
        fields = ['username', 'password', 'code']

    # 返回加密后的密码
    def clean_password(self):
        password = self.cleaned_data.get('password')
        return md5(password)


# 登录功能
def login(request):
    if request.method == 'GET':
        form = LoginModelForm()
        return render(request, 'login.html', {"form": form})

    form = LoginModelForm(data=request.POST)
    # form验证是否有效
    if form.is_valid():
        # print(form.cleaned_data)

        # model = models.Admin.objects.filter(username=form.cleaned_data.get('username'),
        #                                     password=form.cleaned_data.get('password')).exists()

        # {'username': '11', 'password': '163909d762356391c460da09f8802836', 'code': '11das'}
        # 验证码的校验
        # 用户输入的验证码
        user_input_code = form.cleaned_data.pop('code')  # 去除最后一个元素
        # 存储在session中的验证码
        code = request.session.get("image_code", "")
        if user_input_code.upper() != code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {'form': form})
        # 去数据库中校验用户名与密码是否匹配，获取用户对象
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        # 判断数据库中是否存在
        if admin_object:
            # 用户名与密码正确后
            # 网站生成随机的字符串；写到用户浏览器的cookie中；再写到session中

            request.session['info'] = {"id": admin_object.id, "name": admin_object.username}
            # session保存七天，七天后失效
            request.session.set_expiry(60 * 60 * 24 * 7)
            return redirect("/")

    print(form.errors)
    # 在字段上显示错误信息
    # form.add_error('password', '用户名或密码错误')
    return render(request, 'login.html', {"form": form})


# 注销功能
def logout(request):
    """注销"""
    # 清楚当前用户的session，表示退出登录
    request.session.clear()

    return redirect('/login/')


# 随机验证码
def image_code(request):
    """随机验证码生成"""
    # 调用随机验证码的函数
    img, code_string = check_code()

    # print(code_string)  #验证码的数值
    # 将数值存入session，方便后期获取
    request.session['image_code'] = code_string
    # 设置60秒，时间过后验证码失效
    request.session.set_expiry(60)
    stream = BytesIO()  # 创建BytesIO()对象。，由于图片写入内存流
    img.save(stream, 'png')  # 将img写道stream中

    return HttpResponse(stream.getvalue())  # 将内存流中的图像数据作为HTTP响应返回给客户端。stream.getvalue()返回内存流中的二进制数据。
