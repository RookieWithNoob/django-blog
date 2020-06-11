#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: hao 2019/8/12-20:49
import re

from django import forms
from mdeditor.fields import MDTextFormField
# from django_redis import get_redis_connection

# from verification.constants import SMS_CODE_LENGTH
# from verification.forms import mobile_validator
from user.models import User, Message


class RegisterForm(forms.ModelForm):  # 对数据库进行操作的表单应该继承forms.ModelForm，可以自动生成模型中已有的字段。
    """注册表单"""
    # username = forms.CharField(label='用户名', max_length=20, min_length=5,
    #                            error_messages={
    #                                'max_length': '用户名长度要小于20',
    #                                'min_length': '用户名长度要大于4',
    #                                'required': '用户名不能为空'
    #                            })
    # email = forms.CharField(label='邮箱',
    #                            error_messages={
    #                                'required': '邮箱不能为空'
    #                            })
    password = forms.CharField(label='密码', max_length=20, min_length=6,
                               error_messages={
                                   'max_length': '密码长度要小于20',
                                   'min_length': '密码长度要大于5',
                                   'required': '密码不能为空'
                               })
    password_repeat = forms.CharField(label='确认密码', max_length=20, min_length=6,
                                      error_messages={
                                          'max_length': '密码长度要小于20',
                                          'min_length': '密码长度要大于5',
                                          'required': '密码不能为空'
                                      })

    # mobile = forms.CharField(label='手机号码', max_length=11, min_length=11,
    #                          validators=[mobile_validator, ],
    #                          error_messages={
    #                              'max_length': '手机号码长度有误',
    #                              'min_length': '手机号码长度有误',
    #                              'required': '手机号码不能为空'
    #                          })
    # sms_code = forms.CharField(label='短信验证码', max_length=SMS_CODE_LENGTH,
    #                            min_length=SMS_CODE_LENGTH,
    #                            error_messages={
    #                                'max_length': '短信验证码长度有误',
    #                                'min_length': '短信验证码长度有误',
    #                                'required': '短信验证码不能为空'
    #                            })
    class Meta:
        model = User
        fields = ('username', 'email')

    # 当想要详细的提示用户的错误时,建议使用这种单字段校验
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).count():
            raise forms.ValidationError('用户名已存在!')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            raise forms.ValidationError('邮箱格式不正确')

        if User.objects.filter(email=email).count():
            raise forms.ValidationError('邮箱已存在!')

        return email

    # def clean_mobile(self):
    #     mobile = self.cleaned_data.get('mobile')
    #
    #     if not re.match(r'^1[3-9]\d{9}$', mobile):
    #         raise forms.ValidationError('手机号码格式不正确')
    #
    #     if User.objects.filter(mobile=mobile).count():
    #         raise forms.ValidationError('手机号已注册!')
    #
    #     return mobile

    def clean_password2(self):  # 联合校验
        # clean_data = super().clean()
        # 校验密码是否一致
        password = self.clean_data.get('password')
        password_repeat = self.clean_data.get('password_repeat')

        if password != password_repeat:
            raise forms.ValidationError('两次密码不一致,请重试')

        # sms_code = clean_data.get('sms_code')
        # mobile = clean_data.get('mobile')

        # redis_conn = get_redis_connection(alias='verify_code')
        # real_code = redis_conn.get('sms_text_{}'.format(mobile))
        # if (not real_code) or (real_code.decode('utf-8') != sms_code):
        #     raise forms.ValidationError('短信验证码错误!')

        return password


class LoginForm(forms.Form):
    """登录表单"""
    # def __init__(self, *args, **kwargs):  # 在不清楚有什么具体参数的情况下,可使用这种方式代替
    #     self.request = kwargs.pop('request', None)  # 将接收到的request从参数中剔除出来,然后赋值
    #     # 执行完成上面的操作后再去执行父类的init,从而不会破环父类的初始化
    #     super().__init__(*args, **kwargs)

    # 由于不确定是手机号码还是用户名,而这两者的格式是不一样的,所以要单独校验
    # account = forms.CharField(error_messages={'required': '用户名不能为空'})
    username = forms.CharField(error_messages={'required': '用户名不能为空'})
    password = forms.CharField(max_length=20, min_length=6,
                               error_messages={
                                   'max_length': '密码长度要小于20',
                                   'min_length': '密码长度要大于5',
                                   'required': '密码不能为空'
                               })
    remember = forms.BooleanField(required=False)

    # def clean_account(self):
    #     """
    #     用户名校验,也有可能是手机号
    #     :return:
    #     """
    #     account = self.cleaned_data.get('account')
    #
    #     # 如果满足该正则就说明是手机号
    #     if not re.match(r'^1[3-9]\d{9}$', account) and (len(account) < 5 or len(account) > 20):
    #         raise forms.ValidationError('账户格式错误, 请重新输入!')
    #     return account

    # def clean_password(self):
    #     """
    #     校验用户名密码, 并实现登陆逻辑
    #     :return:
    #     """
    #     # clean_data = super().clean()
    #
    #     # 拿到参数
    #     username = self.cleaned_data.get('username')
    #     # account = clean_data.get('account')
    #     password = self.clean_data.get('password')
    #     remember = self.clean_data.get('remember')
    #
    #     # 实现登陆逻辑
    #     # 判断用户名与密码是否匹配
    #     # 1. 先找到这个用户, 使用以下代码来试下这一句sql语句
    #     # select * from tb_users where mobile=account or username=account;
    #     # user_queryset = User.objects.filter(Q(mobile=account) | Q(username=account))
    #     user_queryset = User.objects.get(username=username)
    #     if user_queryset:
    #         # 2. 校验是否匹配'
    #         # user = user_queryset.first()
    #         user = user_queryset
    #         if user.check_password(password):
    #             # 3. 是否免登陆
    #             if remember:
    #                 # 免登陆14天
    #                 self.request.session.set_expiry(USER_SESSION_EXPIRY=14 * 24 * 60 * 60)
    #             else:
    #                 # 关闭浏览器就重置登陆状态
    #                 self.request.session.set_expiry(0)
    #             # 4. 登录
    #             login(self.request, user)
    #         else:
    #             raise forms.ValidationError('用户名密码错误!')
    #
    #     else:
    #         raise forms.ValidationError('该账户不存在,请重新输入!')
    #
    #     return self.clean_data


# ModelForm 可自动将model 对应的字段转为 form字段
class MessageForm(forms.ModelForm):
    """
    留言表单
    """
    # 覆写某字段之后，内部类class Meta中的定义对这个字段就没有效果了，所以fields不用包含。
    # content = MDTextFormField()
    class Meta:
        model = Message
        fields = ['content']
