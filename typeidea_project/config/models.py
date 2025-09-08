from django.db import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string

# Create your models here.
class Link(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    title = models.CharField(max_length=50, verbose_name='标题')
    href = models.URLField(verbose_name='链接') #默认长度200
    status = models.PositiveBigIntegerField(default=STATUS_NORMAL,
                                            choices=STATUS_ITEMS, verbose_name='状态') 
    weight = models.PositiveIntegerField(default=1, choices=zip(range(1, 6),
                                                                range(1, 6)), verbose_name='权重',
                                                                help_text='权重高展示顺序靠前')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = verbose_name_plural = '友链'

class SideBar(models.Model):
    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS_ITEMS = (
        (STATUS_SHOW, '展示'),
        (STATUS_HIDE, '隐藏'),
    )
    DISPLAY_TYPE_HTML = 1
    DISPLAY_TYPE_LATEST = 2
    DISPLAY_TYPE_HOT = 3
    DISPLAY_TYPE_COMMENT = 4
    SIDE_TYPE = (
        (DISPLAY_TYPE_HTML, 'HTML'),
        (DISPLAY_TYPE_LATEST, '最新文章'),
        (DISPLAY_TYPE_HOT, '最热文章'),
        (DISPLAY_TYPE_COMMENT, '最新评论'),
    )

    title = models.CharField(max_length=50, verbose_name='标题')
    display_type = models.PositiveIntegerField(default=1, choices=SIDE_TYPE,
                                               verbose_name='展示类型')
    content = models.CharField(max_length=500, blank=True, verbose_name='内容',
                               help_text='如果设置的不是HTML类型,可为空')
    status = models.PositiveBigIntegerField(default=STATUS_SHOW,
                                            choices=STATUS_ITEMS, verbose_name='状态') 
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = verbose_name_plural = '侧边栏'    
    
    #由于侧边栏的展示类型有HTML、最新文章、最热文章、最新评论
    #所以需要根据不同的展示类型，获取不同的数据，所以从model层获取数据，直接渲染到模板
    @property #@property 是Python的一个内置装饰器，用于将一个方法转换为属性访问方式。{{ sidebar.content_html }}，这是最直观的体现方式
    def content_html(self):
        """直接渲染模版"""
        from blog.models import Post #避免循环引用
        from comment.models import Comment

        result = ''
        if self.display_type == self.DISPLAY_TYPE_HTML:
            result = self.content
        elif self.display_type == self.DISPLAY_TYPE_LATEST:
            context = {
                'posts' : Post.latest_posts()
            }
            result = render_to_string('config/blocks/sidebar_posts.html', context)
        elif self.display_type == self.DISPLAY_TYPE_HOT:
            context = {
                'posts' : Post.hot_posts()
            }
            result = render_to_string('config/blocks/sidebar_posts.html', context)
        elif self.display_type == self.DISPLAY_TYPE_COMMENT:
            context = {
                'comments' : Comment.objects.filter(status=Comment.STATUS_NORMAL)
            }
            result = render_to_string('config/blocks/sidebar_comments.html', context)
        return result
    
    #获取侧边栏的所有数据
    @classmethod
    def get_all(cls):
        return cls.objects.filter(status=cls.STATUS_SHOW)