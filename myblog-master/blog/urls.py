#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from blog import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^archive/$', views.ArchiveView.as_view(), name='archive'),
    url(r'^archive/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})$', views.DateArticleView.as_view(), name='one_archive'),
    url(r'^about/$', views.AboutMeView.as_view(), name='about'),
    url(r'^article/(?P<pk>\d+)$', views.ArticleView.as_view(), name='detail'),
    url(r'^category/(?P<kw>\d+)$', views.OneCategoryView.as_view(), name='one_category'),
    url(r'^category$', views.CategoryView.as_view(), name='category'),
    url(r'^tags/(?P<tag>\d+)$', views.TagsView.as_view(), name='tags'),
]
