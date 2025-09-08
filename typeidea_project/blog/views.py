from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView,  DetailView  
from .models import Post, Tag, Category
from config.models import SideBar

# Create your views here.
class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context

class IndexView(CommonViewMixin, ListView):  # 修复继承顺序
    model = Post
    paginate_by = 1
    context_object_name = 'post_list'
    template_name = 'blog/list.html'
    
    def get_queryset(self):
        return Post.latest_posts()

class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)

class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag_id=tag_id)

class PostDetailView(CommonViewMixin, DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'
    
    def get_queryset(self):
        return Post.latest_posts()
if False:
    def post_list(request, category_id=None, tag_id=None):
        """
        文章列表视图函数，支持按标签和分类筛选
        
        逻辑流程：
        1. 如果提供了tag_id参数：
        - 尝试获取对应的Tag对象
        - 如果Tag不存在，返回空列表
        - 如果Tag存在，获取该标签下所有状态为STATUS_NORMAL的文章
        2. 如果没有提供tag_id参数：
        - 获取所有状态为STATUS_NORMAL的文章
        - 如果提供了category_id参数，进一步筛选属于该分类的文章
        3. 最后将筛选结果传递给模板进行渲染
        
        参数:
            request: HttpRequest对象
            category_id: 可选，分类ID
            tag_id: 可选，标签ID
        
        返回:
            HttpResponse对象，渲染blog/list.html模板
        """
        tag = None
        category =  None

        if tag_id:
            post_list, tag = Post.get_by_tag(tag_id)
        elif category_id:
            post_list, category = Post.get_by_category(category_id)
        else:
            post_list = Post.latest_posts()

        print(f"Tag ID: {tag_id}, Category ID: {category_id}")
        print(f"Post list: {post_list}")

        if hasattr(post_list, 'count'):
            print(f"Number of posts: {post_list.count()}")

        context = {
            'category' : category,
            'tag' : tag,
            'post_list' : post_list,
            'sidebars' : SideBar.get_all(),

        }
        context.update(Category.get_navs())
        print(f"Tag: {tag}")  # 应该显示获取到的Tag对象
        print(f"Category: {category}")  # 应该显示获取到的Category对象
        return render(request, 'blog/list.html', context=context)
        

    def post_detail(request, post_id):
        try:
            # post = Post.objects.get(id=post_id)
            #一次性获取外键关联的所有数据，避免在每次查询中都要再次查询数据库获取外键关联的数据
            post = Post.objects.select_related('category', 'owner').get(id=post_id)
        except Post.DoesNotExist:
            post=None
        context = {
            'post' : post,
            'sidebars' : SideBar.get_all(),
        }
        context.update(Category.get_navs())

        return render(request, 'blog/detail.html', context=context)

