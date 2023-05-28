# -*- coding: utf-8 -*-
# @Author: XuTianDe
# @Date: 2023-05-23 13:48:18
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect


class AuthMiddleware(MiddlewareMixin):
    """是否登录访问中间件"""

    def process_request(self, request):
        # 0.排除不需要登录就可以访问的url地址
        # path_info获取用户当前请求的url

        # 如果当前页面是login则继续执行
        if request.path_info in ['/student/edit/', '/login/', '/image/code/', "/registered/"]:
            return
        # 1.读取当前访问用户的登录信息，登录信息存在则说明登录过，继续执行
        info_dict = request.session.get("info")
        if info_dict:
            return
        # 2.没有登录则
        return redirect('/login/')
        # 如果方法中没有返回值（返回None），继续往后走
        # 如果有返回值 HttpResponse redirect render
        # print('M1中间件进来了')
        # return HttpResponse("m1中间件")  #自己返回HttpResponse对象

    # # return render(request, 'base.html', {"username": info_dict})
    # def process_response(self, request, response):
    #     username=request.session.get("info")
    #     return render(request,'base.html',username)
