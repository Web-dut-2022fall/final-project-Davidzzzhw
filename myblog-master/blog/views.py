from django.shortcuts import render, get_object_or_404
from django.shortcuts import get_list_or_404
from django.views import generic
import markdown
import time

from blog.models import Article, Tags, KeyWord, Category, About


class IndexView(generic.ListView):
    """
    首页视图
    """
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'
    paginate_by = 8


class ArticleView(generic.DetailView):
    """
    文章详情视图
    """
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = 'article_detail'

    def get_object(self):
        obj = super(ArticleView, self).get_object()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            ])
        obj.content = md.convert(obj.content)

        # 设置阅读量限制,设置 5 分钟才能增加
        # 在 session 中设置时间戳,通过有无时间戳和最新时间戳与当前时间戳的之间差
        # 判断是否增加阅读数
        ses = self.request.session
        the_key = 'is_read_{}'.format(obj.id)
        is_read_time = ses.get(the_key)
        if not is_read_time:
            obj.increase_views()
            ses[the_key] = time.time()
        else:
            now_time = time.time()
            t = now_time - is_read_time
            if t > 60*5:
                obj.increase_views()
                ses[the_key] = time.time()
        return obj

    
class OneCategoryView(generic.ListView):
    """
    侧边栏分类视图
    """
    model = Category
    template_name = 'blog/one_category.html'
    context_object_name = 'one_category_list'

    def get_context_data(self, **kwargs):
        """
        添加上下文数据 context,并返回
        返回的是一个字典对象
        """
        context = super(OneCategoryView, self).get_context_data(**kwargs)
        cate_id = self.kwargs.get('kw')
        context['cate_title'] = '文章分类'
        context['cate_article'] = Article.objects.filter(category=cate_id)
        context['cate_name'] = Category.objects.get(id=cate_id)
        return context


class CategoryView(generic.ListView):
    """
    导航栏分类视图
    """
    model = Category
    template_name = 'blog/category_list.html'
    context_object_name = 'category_list'


class TagsView(generic.ListView):
    """
    侧边栏标签视图
    """
    model = Article
    template_name = 'blog/tags.html'
    context_object_name = 'tags_list'

    def get_context_data(self, **kwargs):
        context = super(TagsView, self).get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag')
        # 标签名
        tag = get_object_or_404(Tags, pk=tag_id)
        # 所属标签文章
        tags = self.model.objects.filter(tags=tag_id)
        context['tag_title'] = '文章标签'
        context['tag_art'] = tags
        context['tag_name'] = tag
        return context


class ArchiveView(generic.ListView):
    """
    归档视图
    """
    model = Article
    template_name = 'blog/archive.html'
    context_object_name = 'articles'


class DateArticleView(generic.ListView):
    model = Article
    template_name = 'blog/date_articles.html'
    context_object_name = 'date_articles'

    def get_context_data(self, **kwargs):
        context = super(DateArticleView, self).get_context_data(**kwargs)
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        articles = self.model.objects.filter(release_date__month=month, release_date__year=year)
        context['archive_title'] = '归档'
        context['archive_year'] = year
        context['archive_month'] = month
        context['archive_articles'] = articles
        return context
        

class AboutMeView(generic.ListView):
    model = About
    template_name = 'blog/about.html'
    context_object_name = 'about_me'

    def get_object(self):
        obj = super(AboutMeView, self).get_object()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            ])
        obj.content = md.convert(obj.content)
        return obj

