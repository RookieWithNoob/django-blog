from django.db import models
from django.core.validators import RegexValidator
from db.base_model import BaseModel
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.

mobile_validator = RegexValidator(r'^1[3-9]\d{9}$', '手机号码格式不正确')


# class UserManager(UserManager):
#     """
#     # 修改创建superuser时必须输入email的行为
#     """
#     def create_superuser(self, username, password, email=None, **extra_fields):
#         # 用super调用create_superuser方法创建超级用户
#         super().create_superuser(username=username, password=password, email=email, **extra_fields)
#         # 这种修改源码的操作遵循面向对象大法


class User(AbstractUser, BaseModel):
    '''自定义用户模型类'''

    # mobile = models.CharField('手机号', max_length=11, unique=True, validators=[mobile_validator, ],
    #                           help_text='手机号', error_messages={'unique': "此手机号已注册"})
    IMG_LINK = 'https://img1.doubanio.com/view/group_topic/l/public/p289128177.webp'
    user_image_url = models.CharField('头像链接', max_length=120, default=IMG_LINK, help_text='图片链接')

    class Meta:
        db_table = 'tb_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):  # 调用对象时打印
        return self.username

    # # 通过create superuser命令创建用户时, 需要的字段, 如果不改默认为email
    # REQUIRED_FIELDS = ['mobile']
    #
    # # 管理器实例化为UserManager
    # objects = UserManager()


class Message(BaseModel):
    """
        留言模型
    """
    author = models.ForeignKey('User', verbose_name='评论人', on_delete=models.CASCADE,null=True)
    addr = models.CharField('用户ip地址', max_length=20, help_text='用户的ip地址',null=True, blank=True,)
    content = models.TextField('内容', help_text='内容')
    # 本项目涉及二级评论，修改Comments模型，添加一个parent字段
    parent = models.ForeignKey('self', verbose_name='父留言', on_delete=models.CASCADE, null=True, blank=True, )

    class Meta:
        # ordering = ['-update_time', '-id']
        db_table = 'tb_messages'
        verbose_name = '留言'
        verbose_name_plural = verbose_name

    def __str__(self):
        # django会帮我们在生成迁移的时候自动添加id字段
        return self.content[:20]