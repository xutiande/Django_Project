# -*- coding: utf-8 -*-
# @Author: XuTianDe
# @Date: 2023-05-27 11:51:48
from django.shortcuts import render,HttpResponse

from app01 import models
def city_list(request):
    """城市列表"""
    if request.method =='GET':
        queryset=models.City.objects.all()
        return render(request,'city_list.html',{"queryset":queryset})