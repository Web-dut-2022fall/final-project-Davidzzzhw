from django.contrib import admin
from blog.models import Tags, Category, KeyWord, Article, FriendLink, About


@admin.register(Article)
class ArticleAdim(admin.ModelAdmin):
    list_display = ('id', 'title', 'author',
                    'release_date', 'modify_date',
                    'view', 'delete_status', 'category',
                    )
    list_per_page = 10
    list_editable = ('category',)
    
    # 筛选器
    list_filter = ('release_date', 'category', 'tags', 'keywords', 'is_delete')
    search_fields = ('title', 'release_date', 'id', 'author')
    # 把文章按时间分层
    date_hierarchy = 'release_date'
    ordering = ('-release_date',)

    # 编辑时对多对多字段进行优化
    filter_horizontal = ('tags', 'keywords')


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
   # 设置后台显示内容
   list_display = ('id', 'name') 
   # 分页,设置每页数据
   list_per_page = 10
   # 设置搜索范围
   search_fields = ('name', 'id')
   # 设置默认可编辑字段
   list_editable = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_per_page = 10
    serch_fields = ('name', 'id')
    list_editable = ('name',)


@admin.register(KeyWord)
class KeyWordAdmin(admin.ModelAdmin):
    list_display = ('id', 'keyword')
    list_per_page = 10
    search_fields = ('keyword', 'id')
    list_editable = ('keyword',)


@admin.register(FriendLink)
class FirendLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'link',
                    'create_date')
    list_per_page = 10
    search_fields = ('id', 'name')
    ordring = ('-create_date',)
    list_editable = ('name',)


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('id', 'content')
