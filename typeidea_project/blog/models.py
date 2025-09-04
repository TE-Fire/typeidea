from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    name = models.CharField(max_length=50, verbose_name='名称'),
    status = models.PositiveBigIntegerField(default=STATUS_NORMAL,
                                            choices=STATUS_ITEMS, verbose_name='状态') #用于存储大的正整数(0到9223372036854775807)，通过不同的数值表示不同的状态
    is_nav = models.BooleanField(default=False, verbose_name='是否为导航')  #BooleanField，用于存储布尔值，在数据库中会被映射为布尔类型或小整形，用于标记状态等
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)#当用户被删除时，创建的分类自动被删除
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '分类' #为Model类添加属性

class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=10, verbose_name='名称')
    status = models.PositiveBigIntegerField(default=STATUS_NORMAL,
                                            choices=STATUS_ITEMS, verbose_name='状态')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE) #当用户被删除时，创建的标签自动被删除
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '标签' 

class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )
    title = models.CharField(max_length=255, verbose_name='标题')
    desc = models.CharField(max_length=1024, blank=True, verbose_name='摘要')
    content = models.TextField(verbose_name='正文', help_text='正文必须为MarkDown格式')
    status = models.PositiveBigIntegerField(default=STATUS_NORMAL,
                                            choices=STATUS_ITEMS, verbose_name='状态')
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.PROTECT) #确保不会有文章指向不存在的分类，PROTECT删除模式保护的是被引用的父对象（即外键指向的对象）
    tag = models.ForeignKey(Tag, verbose_name='标签', on_delete=models.PROTECT)
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.SET_NULL, null=True) #删除作者时，将该文章的作者设为null
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id'] #根据id进行降序排列
