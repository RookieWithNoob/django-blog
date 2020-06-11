from django.contrib import admin
from .models import Article, Tags, FriendLink, Comments, HotArticles


# Register your models here.


class ArticleAmdin(admin.ModelAdmin):
    '''设置列表可显示的字段'''
    list_display = ('title', 'author', 'tag', 'views', 'create_time',)

    '''设置过滤选项  搜索'''
    list_filter = ('tag_id', 'create_time',)

    '''每页显示条目数'''
    list_per_page = 10

    '''设置可编辑字段'''
    # list_editable = ('create_time',)

    '''按日期月份筛选'''
    # date_hierarchy = 'create_time'

    '''按发布日期排序'''
    ordering = ('-create_time',)


class TagAmdin(admin.ModelAdmin):
    '''设置列表可显示的字段'''
    list_display = ('id', 'name', 'create_time',)

    '''每页显示条目数'''
    list_per_page = 5

    '''按发布日期排序'''
    ordering = ('-create_time',)


class FriendLinkAmdin(admin.ModelAdmin):
    '''设置列表可显示的字段'''
    list_display = ('name', 'description',  'is_show', 'create_time')

    '''每页显示条目数'''
    list_per_page = 5

    '''按发布日期排序'''
    ordering = ('-create_time',)


class CommentsAmdin(admin.ModelAdmin):
    '''设置列表可显示的字段'''
    list_display = ('author', 'articles', 'parent', 'create_time')

    '''每页显示条目数'''
    list_per_page = 5

    '''按发布日期排序'''
    ordering = ('-create_time',)


class HotArticlesAmdin(admin.ModelAdmin):
    '''设置列表可显示的字段'''
    list_display = ('news', 'priority','create_time',)

    '''每页显示条目数'''
    list_per_page = 5

    '''按发布日期排序'''
    ordering = ('-create_time',)


admin.site.register(Article, ArticleAmdin)
admin.site.register(Tags, TagAmdin)
admin.site.register(FriendLink, FriendLinkAmdin)
admin.site.register(Comments, CommentsAmdin)
admin.site.register(HotArticles, HotArticlesAmdin)
