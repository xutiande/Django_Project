# -*- coding: utf-8 -*-
# @Author: XuTianDe
# @Date: 2023-05-21 22:55:39
from django import forms


class BootStrapModelForm(forms.ModelForm):
    # 简洁样式
    b_exclude_fields = []

    def __init__(self, *args, **kwargs):
        # super父类，重新定义__init__方法
        super().__init__(*args, **kwargs)

        # 获取定义的每个字段
        # 循环给每个字段加入类名class：form-control
        for name, field in self.fields.items():
            # print(name,field)
            if name in self.b_exclude_fields:
                continue

            field.widget.attrs = {'class': 'form-control input-width', "placeholder": field.label, "style": ""}


class LoginBootStrapModelForm(forms.ModelForm):
    # 简洁样式
    def __init__(self, *args, **kwargs):
        # super父类，重新定义__init__方法
        super().__init__(*args, **kwargs)

        # 获取定义的每个字段
        # 循环给每个字段加入类名class：form-control
        for name, field in self.fields.items():
            # print(name,field)
            field.widget.attrs = {'class': 'input-material', "placeholder": field.label, "style": ""}


class BootStrapForms(forms.Form):
    # 简洁样式
    b_exclude_fields = []

    def __init__(self, *args, **kwargs):
        # super父类，重新定义__init__方法
        super().__init__(*args, **kwargs)
        # 获取定义的每个字段
        # 循环给每个字段加入类名class：form-control

        for name, field in self.fields.items():
            # print(name,field)
            if name in self.b_exclude_fields:
                continue
            field.widget.attrs = {'class': 'form-control input-width', "placeholder": field.label, "style": ""}
