from django.urls import path
from django.conf.urls import url, include
from . import views
from .views import ArticleView, TagView, ArticleDetailView, LinkView, AboutView, ArchivesView, CommentView, \
    ArticleSearchView

from rest_framework import routers

# 正在部署的应用的名称
app_name = 'article'

router = routers.DefaultRouter()  # 可以处理视图的路由器
router.register('article_api', views.ArticleAPIView)  # url进行注册

urlpatterns = [
    path('', views.index, name='index'),  # 首页
    path('article/', ArticleView.as_view(), name='article_list'),  # 文章列表
    path('article_detail/<int:article_id>/', ArticleDetailView.as_view(), name='article_detail'),  # 文章详情
    path('article_detail/<int:article_id>/comment/', CommentView.as_view(), name='article_comment'),  # 评论
    path('tag/<int:tag_id>/', TagView.as_view(), name='tag'),  # 文章标签
    path('link/', LinkView.as_view(), name='link'),  # 友情链接
    path('about_me/', AboutView.as_view(), name='about'),  # 关于
    path('archives/', ArchivesView.as_view(), name='archives'),  # 归档
    path('article/search/', ArticleSearchView.as_view(), name='article_search'),  # 搜索
    url(r'^', include(router.urls)),
    url(r'^api/', include('rest_framework.urls', namespace='api'))
]

# urlpatterns += router.urls  # 将路由器中的所有路由信息追加到django的路由列表中
