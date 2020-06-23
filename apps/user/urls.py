from django.urls import path
from . import views
from .views import LoginView, RegisterView, LogoutView, MessageView


# 正在部署的应用的名称
app_name = 'user'


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),  # 用户登录
    path('register/', RegisterView.as_view(), name='register'),  # 用户注册
    path('logout/', LogoutView.as_view(), name='logout'),  # 用户退出
    path('message/', MessageView.as_view(), name='message'),  # 留言

]

