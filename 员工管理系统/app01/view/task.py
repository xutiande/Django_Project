# -*- coding: utf-8 -*-
# @Author: XuTianDe
# @Date: 2023-05-24 09:48:21
import json

from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from app01 import models
from app01.utils.bootstarp import BootStrapModelForm


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"


# ajax学习
def ajax_study(request):
    """学习ajax"""
    return render(request, 'ajax_study.html')


@csrf_exempt
def text_ajax(request):
    """测试ajax"""
    # print(request.POST)
    data_dict = {"status": True, "data": [1, 2, 3]}
    return JsonResponse(data_dict)





def task_list(request):
    """任务管理"""

    if request.method == 'GET':
        queryset = models.Task.objects.all()
        form = TaskModelForm()
        content={
            'form': form,
            'queryset':queryset
        }
        return render(request, "task_list.html", content)


@csrf_exempt
def task_add(request):
    # print(request.POST)
    # "<QueryDict: {'level': ['1'], 'title': ['1'], 'detail': ['1'], 'user': ['1']}>"
    # 获取提交请求的数
    form = TaskModelForm(data=request.POST)
    # 验证是否有效
    if form.is_valid():
        # 验证通过则
        # print(form.cleaned_data)
        form.save()
        data_dict = {"status": True}
        return JsonResponse(data_dict)
    # 否则
    # 将错误信息提交到html
    # form.errors中可以用.as_json输出json格式的错误信息
    data_dict = {"status": False, "errors": form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))  # 改为ensure_ascii中文
