# -*- coding: utf-8 -*-
# @Author: XuTianDe
# @Date: 2023-05-26 09:50:10
from django.shortcuts import render, redirect, HttpResponse

from django.http import JsonResponse


def chart_list(request):
    """数据统计"""
    return render(request, 'chart_list.html')


# 柱状图
def chart_bar(request):
    """构造柱状图的数据"""
    # 数据可以从数据库中获取

    legend = ['销量', '业绩']  # 图例
    series_list = [  # y轴数据
        {
            'name': '销量',
            'type': 'bar',
            'data': [5, 20, 36, 10, 10, 20]
        },
        {
            'name': '业绩',
            'type': 'bar',
            'data': [51, 40, 10, 10, 20, 20]
        },
    ]
    xAxis_list = ['一月', '二月', '三月', '四月', '五月', '六月']  # x轴
    result = {
        "status": True,
        "data": {
            "legend": legend,
            "series_list": series_list,
            "xAxis_list": xAxis_list
        }
    }
    return JsonResponse(result)


# 饼状图
def chart_pic(request):
    """构造饼状图数据据"""
    series_list = [
        {'value': 1048, 'name': 'IT部门'},
        {'value': 735, 'name': '新媒体'},
        {'value': 580, 'name': '运营'},
    ]

    result = {
        "status": True,
        "series_list": series_list
    }
    return JsonResponse(result)


# 折线图
def chart_line(request):
    legend_list = ['Email', 'Union Ads', 'Video Ads', 'Direct', 'Search Engine']
    data_list = ['一月', '二月', '三月', '四月', '五月','六月','七月']
    series_list = [
        [120, 132, 101, 134, 90, 230, 210],
        [220, 182, 191, 234, 290, 330, 310],
        [150, 232, 201, 154, 190, 330, 410],
        [320, 332, 301, 334, 390, 330, 320],
        [820, 932, 901, 934, 1290, 1330, 1320]
    ]
    result = {
        "status": True,
        "data_list": data_list,
        "series_list": series_list
    }
    return JsonResponse(result)
