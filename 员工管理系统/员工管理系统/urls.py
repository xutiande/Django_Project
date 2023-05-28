"""员工管理系统 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,re_path
from app01 import views
from django.views.static import serve
from app01.view import login, task, order, chart, upload,city
from app01 import registered
from django.conf import settings
urlpatterns = [
    # 上传数据目录配置
    re_path(r'^media/(?P<path>.*)$',serve,{"document_root":settings.MEDIA_ROOT},name='media'),

    path('', views.index),
    # 部门管理
    path('depart/list/', views.depart_list),
    path('depart/add/', views.depart_add),
    path('depart/delete/', views.depart_delete),
    path('depart/<int:nid>/edit/', views.depart_edit),
    # 文件上传
    path("depart/multi/", views.depart_multi),

    # 用户管理user_list
    path('user/list/', views.user_list),
    path('user/add/', views.user_add),
    path('user/model/form/add/', views.user_add_modelform),  # modelform表单验证视图
    path('user/delete/<int:nid>/', views.user_delete),
    path('user/<int:nid>/edit/', views.user_edit),

    # 靓号区域
    path('pretty/list/', views.goods_phone_list),
    path('pretty/add/', views.pretty_add),
    path('pretty/<int:nid>/edit/', views.pretty_edit),
    path('pretty/<int:nid>/delete/', views.pretty_delete),

    # 管理员
    path('admin/list/', views.admin_list),
    path('admin/add/', views.admin_add),
    path('admin/<int:nid>/edit/', views.admin_edit),
    path('admin/<int:nid>/delete/', views.admin_delete),
    path('admin/<int:nid>/reset/', views.admin_reset),

    # 注册功能
    path("registered/", registered.registered),
    # 登录功能
    path('login/', login.login),
    # 登录功能
    path('logout/', login.logout),
    # 生成随机验证码
    path("image/code/", login.image_code),

    # 测试任务管理
    path('ajax/study/', task.ajax_study),  # 学习ajax
    path("test/ajax/", task.text_ajax),  # 测试ajax
    path("task/list/", task.task_list),
    path("task/add/", task.task_add),  # 接收ajax传递的数据

    # 订单列表
    path("order/list/", order.order_list),
    path('order/add/', order.order_add),  # 添加
    path("order/delete/", order.order_delete),  # 删除
    path("order/detail/", order.order_detail),
    path("order/edit/", order.order_edit),

    # 数据统计列表
    path("chart/list/", chart.chart_list),
    path('chart/bar/', chart.chart_bar),  # 柱状图
    path("chart/pic/", chart.chart_pic),
    path("chart/line/", chart.chart_line),

    # 上传文件
    path("upload/list/", upload.upload_list),

    path("upload/form/",upload.upload_form),         # form上传
    path("upload/modelform/",upload.upload_modelform),   #modelform上传


    #城市列表
    path("city/list/", city.city_list),
]
