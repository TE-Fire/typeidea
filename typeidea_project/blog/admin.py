from django.contrib.admin.models import LogEntry
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Post, Category, Tag
from .adminforms import PostAdminForm
import requests
from django.contrib.auth import get_permission_codename
from typeidea_project.custom_site import custom_site
from typeidea_project.base_admin import BaseOwnerAdmin
# Register your models here.

class PostInline(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 1 #控制额外多个
    model = Post

@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline, ] #在category操作Post
    list_display = ('name', 'status', 'is_nav', 'owner', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav', 'owner')
    # #将作者设置为登录admin用户，防止随意篡改他人作品为自己的作品
    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user #获取当前登录的用户
    #     return super(CategoryAdmin, self).save_model(request, obj, form, change) #change用于标志本次的数据是更新的还是新增的

    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'
    
@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'owner', 'created_time')
    fields = ('name', 'status', 'owner')
    
    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(TagAdmin, self).save_model(request, obj, form, change)
        
class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户分类"""
    title = '分类过滤器'
    parameter_name = 'owner_category' # 定义 URL 参数名，形如 ?owner_category=1
        
    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name') #获取当前登录用户拥有的所有分类
        
    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value()) #category_id存在并且对其进行过滤
        return queryset
    
PERMISSION_API = "http://permission.sso.com/has_perm?user={}&perm_code={}"
@admin.register(Post, site=custom_site) #site=custom_site，对管理后台功能进行细化，Post为后台用户所见，其他为superuser可见
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm #将其设置为Textarea组件
    list_display = [
        'title', 'category', 'status',
        'created_time', 'operator',
    ]
    list_display_links =[] #展示哪些字段可用来作为链接，点击即可进入编辑

    list_filter = [CategoryOwnerFilter] #配置页面过滤器
    search_fields = ['title', 'category__name'] #双下划线表示指定搜索关联Model数据

    actions_on_top = True #动作相关的配置，展示在顶部
    actions_on_bottom = True #动作相关的配置，展示在底部

    #编辑页面
    save_on_top = True #编辑保存相关的动作展示在顶部
    exclude = ('owner',) #不展示该字段
    
    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )

    #fieldsets用于控制布局，fieldsets = (名称，{内容})，名称是板块的信息，内容是对板块功能的显示等
    fieldsets = (
        ('基础配置',{
            'description' : '基础配置描述',
            'fields' : (
                ('title', 'category'), #将字段放在元组中会垂直水平排列
                'status', #单独列出字段会垂直排列
            ),
        }),
        ('内容', {
            'fields' : (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes' : ('collapse', 'extrapretty',), #classes给要控制的版块添加css样式，collapse使对应的字段集默认显示折叠状态
            'fields' : ('tag', ),
        })
    )

        
    #自定义要在list_display展示的字段
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作' #指定表头的展示文案

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(PostAdmin, self).save_model(request, obj, form, change)
    
    # def get_queryset(self, request):
    #     qs = super(PostAdmin, self).get_queryset(request) #首先获取默认的查询集
    #     return qs.filter(owner=request.user) #过滤出只属于owner的作品
    
    #引入静态资源
    class Media:
        css = {
            'all' : ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css', ),
        }
        js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js', )
    
    #重写django提供的方法，进行权限管理，检查当前用户是否有权限新增文章
    def has_add_permission(self, request):
        opts = self.opts  # 当前模型的信息
        codename = get_permission_codename('add', opts)  # 生成Django标准的权限编码（如：add_post）
        perm_code = f"{opts.app_label}.{codename}"  # 组合成完整权限编码（如：blog.add_post）
        url = PERMISSION_API.format(request.user.username, perm_code)
        try:
            resp = requests.get(url, timeout=3)
            if resp.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.RequestException:
            # 记录日志，或者根据情况返回False
            return False
#为后台增加日志记录
@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(BaseOwnerAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user',
                    'change_message']
    
    def get_queryset(self, request):
        qs = super(admin.ModelAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs  # 超级用户可以看到所有日志
        return qs.filter(user=request.user)  # 普通管理员只能看到自己的日志
    
    def save_model(self, request, obj, form, change):
        # 不需要设置owner字段
        return super(admin.ModelAdmin, self).save_model(request, obj, form, change)