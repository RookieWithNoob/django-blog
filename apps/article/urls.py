from django.urls import path
from . import views
from .views import ArticleView, TagView, ArticleDetailView, LinkView, AboutView, ArchivesView, CommentView

# 正在部署的应用的名称
app_name = 'article'

urlpatterns = [
    path('', views.index, name='index'),  # 首页
    path('article/', ArticleView.as_view(), name='article_list'),  # 文章列表
    path('article_detail/<int:article_id>/', ArticleDetailView.as_view(), name='article_detail'),  # 文章详情
    path('article_detail/<int:article_id>/comment/', CommentView.as_view(), name='article_comment'), # 评论
    path('tag/<int:tag_id>/', TagView.as_view(), name='tag'),  # 文章标签
    path('link/', LinkView.as_view(), name='link'),  # 友情链接
    path('about_me/', AboutView.as_view(), name='about'),  # 关于
    path('archives/', ArchivesView.as_view(), name='archives'),  # 归档
]
