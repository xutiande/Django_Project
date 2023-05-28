# -*- coding: utf-8 -*-
# @Author: XuTianDe
# @Date: 2023-05-26 19:17:53
import os.path

# 上传文件
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django import forms
from app01.utils.bootstarp import BootStrapForms, BootStrapModelForm
from app01 import models
from django.conf import settings


#
def upload_list(request):
    """文件上传"""
    if request.method == 'GET':
        return render(request, 'upload_list.html')
    # enctype="multipart/form-data"
    # 未加前：POST： 'username': ['111'], 'upload_text': ['豆瓣源.txt']}  FILES：{}
    # 家了后：     POST：'username': ['111']            FILES：'upload_text': [<InMemoryUploadedFile: 豆瓣源.txt (text/plain)>]}
    # print(request.POST)  # 请求 体发送过来的数据
    # print(request.FILES)    #请求发过来的文件

    file_object = request.FILES.get("avatar")
    print(file_object.name)
    f = open(file_object.name, mode='wb')

    for chunk in file_object.chunks():  # chunks()分块
        f.write(chunk)
    f.close()
    return HttpResponse("11")


# 上传文件Form验证
class UploadForm(BootStrapForms):
    b_exclude_fields = ['img']
    name = forms.CharField(label='姓名')
    age = forms.IntegerField(label='年龄')
    img = forms.FileField(label='头像')


# form上传
def upload_form(request):
    """文件上传form验证"""
    if request.method == 'GET':
        form = UploadForm()
        return render(request, 'upload_form.html', {"form": form})
    # POST

    form = UploadForm(data=request.POST, files=request.FILES)  # dataPOST请求数据，files文件数据
    if form.is_valid():
        # "{'name': '1', 'age': 2, 'img': <InMemoryUploadedFile: 6664.png_300.png (image/png)>}"
        # 读取内容，对数据进行处理，并进行存储
        # 1.读取图片内容，写入到文件夹中并获取文件的路径
        img_object = form.cleaned_data.get('img')

        # media_path = os.path.join(settings.MEDIA_ROOT, img_object.name)  # 存入数据库的路径,绝对路径  D:\各语言开发目录\django\员工管理系统\media\....
        media_path = os.path.join("media", img_object.name)  # 存入数据库的路径,根目录相对路径     media\....

        # 存入文件夹
        f = open(media_path, mode='wb')
        for chunk in img_object.chunks():
            f.write(chunk)
        f.close()
        # 2.将文件的路径写入到数据库

        models.Boss.objects.create(
            name=form.cleaned_data['name'],
            age=form.cleaned_data['age'],
            img=media_path  # 为图片的路径
        )
        return redirect('/upload/form/')

    return render(request, 'upload_form.html', {"form": form})


class UploadModelForm(BootStrapModelForm):
    b_exclude_fields = ['img']

    class Meta:
        model = models.City
        fields = '__all__'


# modelform上传
def upload_modelform(request):
    """上传文件和数据（modelform）"""
    if request.method == 'GET':
        form = UploadModelForm()
        return render(request, 'upload_modelform.html', {"form": form})
    form = UploadModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 对文件：自动保存到路径
        # 对数据库：字段 + 上传路径到数据库
        form.save()  # "city/6664.png_300.png"
        return redirect("/city/list/")
    return render(request, 'upload_modelform.html', {"form": form})
