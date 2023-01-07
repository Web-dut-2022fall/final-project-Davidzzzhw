from django.db import models
from django.utils.html import format_html, strip_tags
from django.urls import reverse
import markdown


class Tags(models.Model):
    """
    文章标签
    """
    name = models.CharField(max_length=20, verbose_name='标签名')
    
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tags', kwargs={'tag': self.pk})


class Category(models.Model):
    """
    文章分类
    """
    name = models.CharField(max_length=20, verbose_name='分类名称')
    
    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('one_category', kwargs={'kw': self.pk})


class KeyWord(models.Model):
    """
    文章关键词
    """
    keyword = models.CharField(max_length=20, verbose_name='文章关键词')

    class Meta:
        verbose_name = '关键词'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.keyword



class Article(models.Model):
    """
    发布的文章
    """
    title = models.CharField(max_length=30, verbose_name='文章标题')
    describe = models.CharField(max_length=240,blank=True, null=True, verbose_name='文章摘要')
    content = models.TextField(verbose_name='文章内容')
    author = models.CharField(max_length=20, verbose_name='作者')
    release_date = models.DateField(verbose_name='发布时间')
    modify_date = models.DateField(verbose_name='修改时间')
    view = models.IntegerField(default=0, verbose_name='阅读量')
    is_delete = models.BooleanField(default=False, verbose_name='是否被删除')
    delete_status_color = models.CharField(max_length=10, default='green',
                                           verbose_name='设置状态颜色')

    category = models.ForeignKey(Category, verbose_name='文章分类')
    tags = models.ManyToManyField(Tags, verbose_name='文章标签')
    keywords = models.ManyToManyField(KeyWord, verbose_name='文章关键词',
                                      help_text='文章关键词,SEO 优化')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-release_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})

    def get_archive_url(self):
        return reverse('one_archive', kwargs={'year': self.release_date.year,
                                              'month': self.release_date.month
                                              })

    def delete_status(self):
        # 设置是否删除状态的颜色
        if self.is_delete:
            self.delete_status_color = 'red'
        return format_html(
                   '<span style="color:{};">{}</span>',
                   self.delete_status_color,
                   self.is_delete,
               )
    delete_status.short_description = '是否被删除'

    def increase_views(self):
        self.view += 1
        self.save(update_fields=['view'])

    def content_to_markdown(self):
        return markdown.markdown(self.content, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            ])
            
    def save(self, *args, **kwargs):
        """
        自动提取摘要
        """
        if not self.describe:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                ])
            self.describe = strip_tags(md.convert(self.content))[:60]
        super(Article, self).save(*args, **kwargs)
        

class FriendLink(models.Model):
    """
    友情链接
    """
    name = models.CharField(max_length=50, verbose_name='网站名称')
    description = models.CharField(max_length=100, blank=True, null=True,
                                   verbose_name='网站描述')
    link = models.CharField(max_length=255, verbose_name='友情链接')
    logo_link = models.CharField(max_length=255, verbose_name='logo 链接')
    create_date = models.DateField(verbose_name='添加时间')
    is_active = models.BooleanField(default=True, verbose_name='是否有效')
    
    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']

    def __str__(self):
        return self.name


class About(models.Model):
    """
    关于我
    """
    content = models.TextField(verbose_name='关于我')

    class Meta:
        verbose_name = '关于我'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content

    def save(self, *args, **kwargs):
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            ])
        self.content = md.convert(self.content)
        super(About, self).save(*args, **kwargs)
