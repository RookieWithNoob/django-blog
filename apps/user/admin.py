from django.contrib import admin
from .models import User, Message, MessagesReply


# Register your models here.


class UserAmdin(admin.ModelAdmin):
    '''设置列表可显示的字段'''
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'create_time',)

    '''设置过滤选项  搜索'''
    list_filter = ('is_superuser', 'create_time',)

    '''每页显示条目数'''
    list_per_page = 10

    '''设置可编辑字段'''
    list_editable = ('is_staff',)

    '''按日期月份筛选'''
    # date_hierarchy = 'create_time'

    '''按发布日期排序'''
    ordering = ('create_time',)


class MessageAmdin(admin.ModelAdmin):
    '''设置列表可显示的字段'''
    list_display = ('author', 'create_time',)

    '''设置过滤选项  搜索'''
    list_filter = ('author', 'create_time',)

    '''每页显示条目数'''
    list_per_page = 10

    '''按发布日期排序'''
    ordering = ('-create_time',)


class MessagesReplyAmdin(admin.ModelAdmin):
    '''设置列表可显示的字段'''
    list_display = ('author_from', 'author_to','create_time')

    '''设置过滤选项  搜索'''
    list_filter = ('create_time',)

    '''每页显示条目数'''
    list_per_page = 10

    '''按发布日期排序'''
    ordering = ('-create_time',)

admin.site.register(User, UserAmdin)
admin.site.register(Message, MessageAmdin)
admin.site.register(MessagesReply, MessagesReplyAmdin)

