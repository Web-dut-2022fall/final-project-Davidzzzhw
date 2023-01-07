from django.contrib.syndication.views import Feed
from django.conf import settings

from .models import Article

class AllArticleRssFeed(Feed):
    """
    生成 RSS 订阅
    """
    title = settings.SITE_AND_TITLE
    link = settings.SITE_LINK
    description = settings.SITE_DESCRIPTION

    def items(self):
        return Article.objects.all()

    def item_title(self, item):
        return '[{}]{}'.format(item.category, item.title)

    def item_description(self, item):
        return item.content_to_markdown()
