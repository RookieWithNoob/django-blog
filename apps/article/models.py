from django.db import models
# 抽象模型类
from db.base_model import BaseModel
from mdeditor.fields import MDTextField



# class ArticleManager(models.Manager):
#     """
#     文章归档管理器
#     """
#     def distinct_date(self):  # 该管理器定义了一个distinct_date方法，目的是找出所有的不同日期
#         distinct_date_list = []  # 建立一个列表用来存放不同的日期 年-月
#         date_list = self.values('create_time')  # 根据文章字段create_time 创建时间 找出所有文章的发布时间
#         for date in date_list:  # 对所有日期进行遍历，当然这里会有许多日期是重复的，目的就是找出多少种日期
#             date = date['create_time'].strftime('%Y/%m 存档') # 取出一个日期改格式为 ‘xxx年/xxx月 存档’
#             if date not in distinct_date_list:
#                 distinct_date_list.append(date)
#         return distinct_date_list

"""上文代码建立的管理器需要在文章模型类加上语句：objects = ArticleManager()  ，然后就可以调用 distinct_date 方法了： 
archive_list = Article.objects.distinct_date()，

对比：
article_list = Article.objects.all() # 获取所有文章，获取到的是所有文章对象的一个列表

archive_list = Article.objects.distinct_date()  # 文章归档 获取到的列表格式为： xxx年/xxx月 存档"""

class Tags(BaseModel):
    """
    文章标签模型
    """
    name = models.CharField('标签名', max_length=64, help_text='标签名')

    class Meta:
        # ordering = ['-update_time', '-id']  # 排序, 负号表示为倒叙
        db_table = 'tb_tag'  # 指明数据库表名
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        # str使类实例直接被打印时也会有返回值
        return self.name


# 博客文章数据模型
class Article(BaseModel):
    """
    文章模型
    """

    # 文章作者。参数 on_delete 用于指定数据删除的方式
    # django可以识别`appname.User`这种方式的引用
    author = models.ForeignKey('user.User', verbose_name='文章作者',on_delete=models.CASCADE)

    # 文章标题。models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    title = models.CharField('标题', max_length=150, help_text='标题')

    summary = models.TextField('文章摘要', max_length=230, help_text='摘要', default='文章摘要等同于网页description内容，请务必填写...')

    content = MDTextField('内容', help_text='内容')

    views = models.IntegerField('阅览量', default=0, help_text='浏览量')

    status_choices = (
        (0, '转载'),
        (1, '原创'),
    )
    attributes = models.SmallIntegerField('是否原创', choices=status_choices, default=1)

    IMG_LINK = '/image/two.jpg'
    image_url = models.CharField('图片链接', max_length=200, default=IMG_LINK, help_text='图片链接')

    # 定义分类标签的外键字段, 一般外键字段定义在`一对多`中多的一方
    tag = models.ForeignKey('Tags', verbose_name='文章标签',on_delete=models.SET_NULL, null=True)

    # 实现文章归档
    # objects = ArticleManager()  # 在模型中使用自定义的管理器

    class Meta:
        # ordering = ['-update_time', '-id']
        db_table = 'tb_articles'
        verbose_name = '博客文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class FriendLink(BaseModel):
    """
    友情链接
    """
    status_choices = (
        (0, '无效'),
        (1, '有效'),
    )
    name = models.CharField('网站名称', max_length=50)
    description = models.CharField('网站描述', max_length=100, blank=True)
    link = models.URLField('友链地址', help_text='请填写http或https开头的完整形式地址')
    logo = models.URLField('网站LOGO', help_text='请填写http或https开头的完整形式地址', blank=True)
    create_date = models.DateTimeField('创建时间', auto_now_add=True)
    is_active = models.SmallIntegerField('是否有效', choices=status_choices, default=1)
    is_show = models.BooleanField('是否首页展示', default=False)

    class Meta:
        db_table = 'tb_FriendLink'
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        # ordering = ['create_date']

    def __str__(self):
        return self.name


class Comments(BaseModel):
    """
    评论模型
    """
    content = models.TextField('内容', help_text='内容')

    author = models.ForeignKey('user.User', verbose_name='评论人',on_delete=models.CASCADE, null=True)
    # CASCADE级联删除, 若新闻文章被删除, 那么评论也将被删除
    articles = models.ForeignKey('Article', verbose_name='所属文章',on_delete=models.CASCADE)

    # 本项目涉及二级评论，修改Comments模型，添加一个parent字段
    parent = models.ForeignKey('self', verbose_name='父评论',on_delete=models.CASCADE, null=True, blank=True, )

    # rep_to = models.ForeignKey('self', verbose_name='回复',
    #                            blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        # ordering = ['-update_time', '-id']
        db_table = 'tb_comments'
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        # django会帮我们在生成迁移的时候自动添加id字段
        return self.content[:20]

    def to_dict_data(self):
        comment_dict = {
            'news_id': self.articles_id,
            'content_id': self.id,
            'content': self.content,
            'author': self.author.username,
            'create_time': self.create_time.astimezone().strftime('%Y年%m月%d日 %H:%M'),
            'parent': self.parent.to_dict_data() if self.parent else None
        }
        # comment_dict = Comments.objects.to_dict_data() # 获取到的字典格式为： comment_dict
        return comment_dict


class HotArticles(BaseModel):
    """
    新闻文章模型
    """
    news = models.OneToOneField('Article', verbose_name='文章',on_delete=models.CASCADE)
    priority = models.IntegerField('优先级', help_text='首页热门文章优先级')

    class Meta:
        # ordering = ['-update_time', '-id']  # 排序
        db_table = "tb_hot_articles"  # 指明数据库表名
        verbose_name = "热门文章"  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    def __str__(self):
        return '<热门新闻{}>'.format(self.id)
