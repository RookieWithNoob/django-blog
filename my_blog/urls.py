"""my_blog URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

admin.site.site_title = '博客管理后台'
admin.site.site_header = '博客管理后台'

urlpatterns = [
    path('admin/', admin.site.urls),
    # 新增代码，配置app的url
    path('', include('article.urls', namespace='article')),  # 文章模块
    # 用户注册登陆页
    path('user/', include('user.urls', namespace='user')),  # 用户模块
    path('password-reset/', include('password_reset.urls')),  # 重置密码
    path('mdeditor/', include('mdeditor.urls'), ),  # 富文本
    # path('accounts/', include('allauth.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='api'))
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 富文本需要的配置
