from django.urls import path
from . import views
from .views import LoginView, RegisterView, LogoutView, MessageView
from rest_framework import routers
from django.conf.urls import url, include

# 正在部署的应用的名称
app_name = 'user'

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),  # 用户登录
    path('register/', RegisterView.as_view(), name='register'),  # 用户注册
    path('logout/', LogoutView.as_view(), name='logout'),  # 用户退出
    path('message/', MessageView.as_view(), name='message'),  # 留言

    url(r'^', include(router.urls)),

]
