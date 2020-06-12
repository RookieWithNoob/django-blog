from django.shortcuts import render, redirect, reverse, get_object_or_404
import logging
# 引入markdown模块
import markdown
from django.views.generic import View
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage  # 分页
from haystack.generic_views import SearchView  # 搜索
from django.conf import settings
# 导入数据模型ArticlePost
from .models import HotArticles, Article, Tags, FriendLink, Comments
from .form import CommentForm

# Create your views here.

logger = logging.getLogger('django')


# 视图函数
# 127.0.0.1:8000/
def index(request):
    # 通过外键获取新闻的标题和图片,并按照点击量降序的方式, 抽取3篇最热门的文章
    hot_articles = HotArticles.objects.select_related('news').only(
        'news__title', 'news__image_url', 'news__create_time', 'news__summary'
    ).filter(is_delete=False).order_by('priority', '-news__views')[:3]

    return render(request, 'index/index.html',
                  context={
                      'hot_articles': hot_articles,
                  })


# /article
class ArticleView(View):
    """
    文章页
    """

    def get(self, request):
        # 1. 获取参数
        # 使用异常处理搞定出现的数据错误
        # try:
        #     tag_id = int(request.GET.get('tag_id', 0))  # 默认为0
        # except Exception as e:
        #     # 若出错, 则记录日志, 依然给tag默认值0
        #     logger.error('标签错误: \n{}'.format(e))
        #     tag_id = 0
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

        # 获取所有文章
        articles_list = Article.objects.filter(is_delete=False).order_by('-create_time')

        # 4. 分页, PER_PAGE_NEWS_COUNT常量定义为5
        paginator = Paginator(articles_list, 5)
        # 获取页面数据, get_page可以容错
        articles = paginator.get_page(page)

        # # 显示的总页数
        # total_page = page.num_pages

        # 通过外键获取新闻的标题,并按照点击量降序的方式, 抽取8篇最热门的文章
        hot_articles = Article.objects.only(
            'title', ).filter(is_delete=False).order_by('-views')[:8]
        # 需要传递给模板（templates）的对象
        context = {'articles': articles,
                   'hot_articles': hot_articles, }
        # render函数：载入模板，并返回context对象
        return render(request, 'article/article_list.html', context)


# /tag/<int:tag_id>/
class TagView(View):
    """
    标签页
    """

    def get(self, request, tag_id):
        try:
            tag = Tags.objects.get(id=tag_id)
        except Exception as e:
            # 若出错, 则记录日志, 依然给tag默认值0
            logger.error('标签错误: \n{}'.format(e))
            return redirect(reverse("article:article_list"))
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
        # 获取标签下所有文章
        # 通过多类的条件查询一类的数据：
        #     一类名.objects.filter(多类名小写__多类属性名__条件名)   # 关联属性没有定义在该类中,所以用多类名小写
        # 通过一类的条件查询多类的数据：
        #     多类名.objects.filter(关联属性__一类属性名__条件名)   # 关联属性定义在该类中,所以直接用关联属性名
        articles_list = Article.objects.filter(is_delete=False, tag__name=tag.name).order_by('-create_time')
        paginator = Paginator(articles_list, 5)
        articles = paginator.get_page(page)
        return render(request, 'article/article_list.html', {'articles': articles, })


# article_detail/<int:article_id>/
class ArticleDetailView(View):
    """
    文章详情页
    """

    def get(self, request, article_id):
        #  取出文章内容
        article = Article.objects.get(id=article_id)

        # 取出文章评论
        # comments = Comments.objects.filter(article=article_id) 'comments': comments
        # 将markdown语法渲染成html样式
        article.content = markdown.markdown(article.content,
                                            extensions=[
                                                # 包含 缩写、表格等常用扩展
                                                'markdown.extensions.extra',
                                                # 语法高亮扩展
                                                'markdown.extensions.codehilite',
                                                'markdown.extensions.toc',
                                            ])

        return render(request, 'article/article_detail.html', {'article': article,
                                                               })


# article_detail/<int:article_id>/comment
class CommentView(View):
    """
    添加评论视图
    """

    def post(self, request, article_id):
        # get_object_or_404()：它和Model.objects.get()的功能基本是相同的。区别是在生产环境下，如果用户请求一个不存在的对象时，
        # Model.objects.get()会返回Error 500（服务器内部错误），
        # 而get_object_or_404()会返回Error 404。相比之下，返回404错误更加的准确。
        article = get_object_or_404(Article, id=article_id)
        # 是否登录, 通过is_authenticated的值来判断
        if not request.user.is_authenticated:
            # 若未登录, 则抛出session错误: "用户未登录"
            return redirect(reverse('user:login'))

        # 文章是否存在, 通过数据库查询来判断
        # if not Article.objects.only('id').filter(is_delete=False, id=article_id).exists():
        #     return HttpResponse("文章不存在!!!")

        # 获取评论内容
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            content = comment_form.cleaned_data.get('content')
            # 评论父id是否正常
            # parent_id = comment_form.cleaned_data.get('parent_id')
            # if parent_id:
            #     try:
            #         parent_id = int(parent_id)
            #         if not Comments.objects.only('id').filter(is_delete=False, id=parent_id, news_id=news_id).exists():
            #             return json_response(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
            #     except Exception as e:
            #         logger.info('前端传递的parent_id异常\n{}'.format(e))
            #         return json_response(errno=Code.PARAMERR, errmsg='未知异常')

            # 保存到数据库
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.content = content
            # comment.parent_id = parent_id if parent_id else None
            comment.save()

            return redirect(reverse('article:article_detail', args=[article_id]))


# link/
class LinkView(View):
    """
    友情链接页
    """

    def get(self, request):
        link_list = FriendLink.objects.filter(is_delete=False, is_show=True, is_active=1)
        return render(request, 'link/link.html', {'link_list': link_list})


# about_me/
class AboutView(View):
    """
    关于页
    """

    def get(self, request):
        return render(request, 'about_me.html')


# archives/
class ArchivesView(View):
    """
    归档页
    """

    def get(self, request):
        archives = Article.objects.all()
        return render(request, 'archives/archives.html', {'archives': archives})





class ArticleSearchView(SearchView):
    """
    博客搜索视图
    """
    # 设置搜索模板文件
    template_name = 'article/search.html'

    # 重写get请求，如果请求参数q为空，返回模型News的热门新闻数据
    # 否则根据参数q搜索相关数据
    def get(self, request, *args, **kwargs):
        # 1. 获取查询参数
        query = request.GET.get('q')
        # 2. 如果没有查询参数
        if not query:
            # 则返回博客列表
            # 获取热门新闻对象, 包含外键标签, 查询数据并做筛选和排序
            articles_list = Article.objects.filter(is_delete=False).order_by('-create_time')
            # 分页, 从配置文件中拿到haystack参数
            # paginator = Paginator(articles_list, 1)
            paginator = Paginator(articles_list, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE)
            try:
                # 拿到前端传递的page,
                page = paginator.get_page(int(request.GET.get('page')))
            except Exception as e:
                # 如果出错则返回第一页,保证容错性
                page = paginator.get_page(1)


            return render(request, self.template_name, context={
                'page': page,
                # 'paginator': paginator,
                'query': query,
            })
        # 3. 如果有查询参数
        else:
            # 则执行搜索
            return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        """
        在context中添加page变量
        """
        context = super().get_context_data(*args, **kwargs)
        if context['page_obj']:
            # 捕获page_obj,将其赋值到page
            context['page'] = context['page_obj']
        return context
