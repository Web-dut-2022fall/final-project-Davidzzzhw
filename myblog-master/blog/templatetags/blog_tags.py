from django import template
from django.db.models.aggregates import Count
from django.shortcuts import get_list_or_404

from blog.models import Article, Tags, Category, About

register = template.Library()

@register.simple_tag
def get_keywords(artt):
    """
    获取文章关键词
    """
    keywords = artt.keywords.all()
    return ','.join([keyword.keyword for keyword in keywords])

@register.simple_tag
def new_article_list(num=3):
    """
    获取最新文章
    """
    new_article =  Article.objects.filter(is_delete=False).order_by('-release_date')[:num]
    return new_article

@register.simple_tag
def get_tags():
    """
    获取标签下大于 1 的文章数的标签
    """
    return Tags.objects.annotate(num_article=Count('id')).filter(num_article__gt=0)

@register.simple_tag
def get_categorys():
    """
    获取文章数大于 1 的分类
    """
    return Category.objects.annotate(count_article=Count('article')).filter(count_article__gt=0)

@register.simple_tag
def get_archives():
    """
    按月归档
    """
    return Article.objects.dates('release_date', 'month', order='DESC')

@register.simple_tag
def category_article(cate):
    """
    获取某分类/标签下的所有文章
    """
    return Article.objects.filter(category=cate)

