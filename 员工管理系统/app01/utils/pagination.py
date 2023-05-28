# -*- coding: utf-8 -*-
# @Author: XuTianDe
# @Date: 2023-05-21 16:28:36

"""
    自定义的分页组件,以后使用这个分页组件,需要做以下的事
在视图函数中:
    def goods_phone_list(request):
        # 分页
        from app01.utils.pagination import Pagination
        1.筛选需要的数据
        queryset = models.PrettyNum.objects.filter(**data_list).order_by('-level')

        2.在page_objects内对数据进行处理
        page_objects = Pagination(request, queryset)  # 将参数传递给组件

        3.将处理后的数据渲染到HTML
        # 传递的所有数据
        content = {'queryset': page_objects.queryset,  # 分页完成的数据
                   "search_data": search_data,
                   "page_string": page_objects.html(),  # # 获取定义方法的返回值   页码
                   "all_count": page_objects.total_page_count
                   }
        return render(request, 'pretty_list.html', content)
在HTML中:
    渲染所有的数据:
    {% for i in queryset %}
        {{i......}}
    {% endfor %}


    底部的页码标签组件:
      <div style="text-align: center;">
            <nav aria-label="Page navigation example" style="display: inline-block">
                <ul class="pagination" style="">
                    {{ page_string }}
                    <form class="d-flex"  method="post">
                        {% csrf_token %}
                        <input class="form-control me-2" type="search" name='go_page' style="width:80px;margin-left: 10px">
                        <button class="btn btn-outline-success" type="submit">Go</button>
                    </form>
                    <span style="font-size: 12px;padding: 18px 0 0 15px">共  <b> {{ all_count }}</b> 条数据</span>
                </ul>
            </nav>
"""
from django.utils.safestring import mark_safe


class Pagination(object):
    def __init__(self, request, queryset, page_size=10, page_param="page"):
        """

        :param request: 请求对象
        :param queryset:查询的符合条件数据.会根据这个数据进行分页处理
        :param page_size:每页显示多少条数据
        :param page_param:在url中获取分页的参数,例如/pretty/list/?page=....
        """
        # 1 处理bug,分页+搜索情况下翻页会清空搜索条件
        import copy
        # 2
        query_dict = copy.deepcopy(request.GET)
        # 3
        query_dict._mutable = True  # 修改默认参数,使得可以修改URL
        # query_dict.setlist("page", [1])  # url中页码等于多少
        # print(query_dict.urlencode()) #页码的参数
        # 4
        self.query_dict = query_dict

        page = request.GET.get(page_param, '1')  # 获取URL地址的输入值
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.start = (page - 1) * page_size  # 起始值
        self.end = page * page_size  # 结束值
        self.page_size = page_size  # page_size显示数据的条数
        self.queryset = queryset[self.start:self.end]  # order_by排序,-level为以该字段名降序排序
        self.page_param = page_param
        # 计算符合条件的数据条数
        self.total_count = queryset.count()  # 总数据条数

        # 得出html中的每一个a标签数量
        self.total_page_count = (self.total_count // self.page_size)  +1# 总页码

        # 计算出当前页的前两页与后两页
        self.start_page = self.page - 2
        self.end_page = self.page + 2

    def html(self):
        # 1.起始值不能是负数
        if self.start_page <= 0:
            self.start_page = 1
        # 页码
        page_str_list = []

        for i in range(self.start_page, self.end_page + 1):
            # 2.结束的页面不能超过总页码
            if i <= self.total_page_count:
                if i == self.page:
                    # 5
                    self.query_dict.setlist(self.page_param, [i])  # i为页码

                    # 6
                    ele = f'<li class="page-item active"><a class="page-link " href="?{self.query_dict.urlencode()}">{i}</a></li>'
                else:
                    self.query_dict.setlist(self.page_param, [i])
                    ele = f'<li class="page-item"><a class="page-link "href="?{self.query_dict.urlencode()}">{i}</a></li>'
                page_str_list.append(ele)

        page_string = mark_safe("".join(page_str_list))  # mark_safe包裹证明是安全的
        return page_string
