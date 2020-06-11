from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from .forms import RegisterForm, LoginForm, MessageForm
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage  # 分页
from django.contrib.auth import authenticate, login, logout
import logging
import requests
# import markdown
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from user.models import User, Message

logger = logging.getLogger('django')


# Create your views here.

# /user/login
class LoginView(View):
    """
    用户登录
    """

    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        # 1.校验参数
        user_login_form = LoginForm(data=request.POST, )
        if user_login_form.is_valid():
            # .cleaned_data 清洗出合法数据 拿到参数
            username = user_login_form.cleaned_data.get('username')
            password = user_login_form.cleaned_data.get('password')
            remember = user_login_form.cleaned_data.get('remember')

            # 获取登录后所要跳转到的地址
            # 默认跳转到首页
            next_url = request.GET.get('next', reverse("article:article_list"))

            # 跳转到next_url
            response = redirect(next_url)  # HttpResponseRedirect

            # 检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个 user 对象
            user = authenticate(username=username, password=password)
            if user:
                # 3. 是否免登陆
                if remember:
                    # 免登陆14天
                    request.session.set_expiry(14 * 24 * 60 * 60)
                    # response.set_cookie('username', username, max_age=7 * 24 * 3600)
                else:
                    # 关闭浏览器就重置登陆状态
                    request.session.set_expiry(0)
                    # response.delete_cookie('username')
                # 4. 登录
                login(request, user)

                return response
            else:
                return render(request, 'user/login.html', {'errmsg': '用户名或密码错误喔~请重新输入'})
        else:
            return render(request, 'user/login.html', {'errmsg': '用户名或密码格式不正确~请重新输入'})


# /user/logout
class LogoutView(View):
    """
        登出视图
    """

    def get(self, request):
        logout(request)

        return redirect(reverse('article:article_list'))


# /user/register
class RegisterView(View):
    """
    用户注册
    """

    def get(self, request):
        return render(request, 'user/register.html', )

    def post(self, request):
        # 1.校验参数
        user_register_form = RegisterForm(data=request.POST)
        if user_register_form.is_valid():
            # .cleaned_data 清洗出合法数据 拿到参数
            username = user_register_form.cleaned_data.get('username')
            password = user_register_form.cleaned_data.get('password')
            email = user_register_form.cleaned_data.get('email')
            # print(username)
            # print(password)
            # print(email)
            # 进行业务处理: 进行用户注册
            User.objects.create_user(username, email, password)
            return redirect(reverse('user:login'))
        else:
            return render(request, 'user/register.html', {'errmsg': '注册失败~(数据格式不正确/用户名或邮箱已存在/其它原因)'})


# 根据请求ip获取地区
def get_ip_address(ip):
    response = requests.get('http://ip.ws.126.net/ipquery?ip={}'.format(ip))
    a = response.text.split()[1].split('=')[1].split(',')[0].split('"')[1]
    b = response.text.split()[2].split('=')[1].split(';')[0].split('"')[1]
    print(response.text.split()[2].split('=')[1].split(';')[0].split('"')[1])
    print(response.text.split()[1].split('=')[1].split(',')[0].split('"')[1])
    return a + b

# message/
class MessageView(View):
    """
    留言页
    """

    def get(self, request):
        # # 引入评论表单
        # message_form = MessageForm()
        try:
            page = int(request.GET.get('page', 1))  # 默认为1

        except PageNotAnInteger:
            logger.error('页码错误: \n{}'.format(PageNotAnInteger))
            # 如果请求的页数不是整数, 返回第一页。
            page = 1
        except InvalidPage:
            logger.error('页码错误: \n{}'.format(InvalidPage))
            # 如果请求的页数不存在, 重定向页面
            return redirect(reverse("article:article_list"))
        except Exception as e:
            # 若出错, 则记录日志, 依然给tag默认值0
            logger.error('页码错误: \n{}'.format(e))
            page = 1

        # 获取所有留言
        messages_list = Message.objects.filter(is_delete=False).order_by('-create_time')

        # 4. 分页, PER_PAGE_NEWS_COUNT常量定义为5
        paginator = Paginator(messages_list, 8)
        # 获取页面数据, get_page可以容错
        messages = paginator.get_page(page)

        context = {'messages': messages,
                   'messages_list': messages_list,}
                   # 'message_form':message_form}
        return render(request, 'message/message.html', context)

    # @login_required()
    def post(self, request):
        # 1.校验参数
        # print("**************************************************************************")
        message_form = MessageForm(data=request.POST, )
        print(message_form)
        if message_form.is_valid():
            user = request.user
            if user.is_authenticated:
                # 保存数据，但暂时不提交到数据库中
                content = message_form.cleaned_data.get('content')
                message = message_form.save(commit=False)
                message.author = request.user
                message.content = content
                # message.content = markdown.markdown(content,
                #                          extensions=[
                #                              # 包含 缩写、表格等常用扩展
                #                              'markdown.extensions.extra',
                #                              # 语法高亮扩展
                #                              'markdown.extensions.codehilite',
                #                              'markdown.extensions.toc',
                #                          ])
                print(request.META['REMOTE_ADDR'])
                # 获取地区
                message.addr = get_ip_address('171.83.97.52')
                # 将新文章保存到数据库中
                message.save()
                return redirect(reverse('user:message'))
            else:
                return redirect(reverse('user:login'))
        else:
            return HttpResponse("表单内容有误，请重新填写。")
