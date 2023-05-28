# -*- coding: utf-8 -*-
# @Author: XuTianDe
# @Date: 2023-05-25 13:51:28
import random
from datetime import datetime
from django.shortcuts import render, redirect, HttpResponse

from app01.utils.bootstarp import LoginBootStrapModelForm
from app01 import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app01.utils import pagination


class OrderModelForm(LoginBootStrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        # 排除该字段
        exclude = ["oid", 'admin']


def order_list(request):
    queryset = models.Order.objects.all()  # 数据
    page_objects = pagination.Pagination(request, queryset)  # 传入
    form = OrderModelForm()  # 表单

    content = {
        'queryset': page_objects.queryset,  # 分页完成的数据
        "page_string": page_objects.html(),  # # 获取定义方法的返回值   页码
        "all_count": page_objects.total_page_count,
        "form": form
    }
    return render(request, 'order_list.html', content)


# ajax处理请求
@csrf_exempt
def order_add(request):
    """新建订单(处理ajax请求)"""
    form = OrderModelForm(data=request.POST)
    # 通过表单验证后
    if form.is_valid():
        # 此时oid为空，oid为后台自动生成
        # {'title': '2', 'price': 1, 'status': 1, 'admin': < Admin: 徐天德 >}
        # 随机生成oid
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(100, 999))
        # print(request.session.items())
        # 字段admin为当前登录系统的用户
        form.instance.admin_id = request.session['info']['id']
        form.save()
        data_dist = {"status": True}
        return JsonResponse(data_dist)
    data_dist = {"status": False, "error": form.errors}
    return JsonResponse(data_dist)


def order_delete(request):
    """删除订单"""
    nid = request.GET.get("nid")
    exists = models.Order.objects.filter(id=nid).exists()
    if exists:
        models.Order.objects.filter(id=nid).delete()
        data_dict = {"status": True}
        return JsonResponse(data_dict)

    data_dict = {"status": False, "error": "删除失败,数据不存在"}
    return JsonResponse(data_dict)


# 编辑
def order_detail(request):
    """编辑订单对话框"""

    if request.method == 'GET':
        uid = request.GET.get("uid")
        # now_object是一个对象，通过now_object.id...获取数据   通过.values(....)可以直接获取里面的值
        now_object = models.Order.objects.filter(id=uid).values("title", "price", "status").first()
        if not now_object:
            data_dict = {"status": False, "error": "数据不存在"}
            return JsonResponse(data_dict)

        result = {
            "status": True,
            "data": now_object
        }

        return JsonResponse(result)


# 编辑提交POST
@csrf_exempt
def order_edit(request):
    uid = request.GET.get("uid")
    now_object = models.Order.objects.filter(id=uid).first()
    # 如果没有该id的数据
    if not now_object:
        return JsonResponse({"status": False, "tips": '数据不存在'})
    # 有则
    form = OrderModelForm(data=request.POST, instance=now_object)
    if form.is_valid():
        form.save()

        result = {
            "status": True,
        }
        return JsonResponse(result)
    return JsonResponse({"status": False, "error": form.errors})
