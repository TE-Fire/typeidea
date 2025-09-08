"""
URL configuration for typeidea_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .custom_site import custom_site
from blog.views import (
    IndexView, CategoryView, TagView,
    PostDetailView,
)
# from blog.views import post_detail, post_list
from config.views import links

urlpatterns = [
    #在同一套后台管理的逻辑上分化出对后台管理的不同功能
    path('super_admin/', admin.site.urls, name='super-admin'),
    path('admin/', custom_site.urls, name='admin'),
    # 匹配空路径（首页）
    path('', IndexView.as_view(), name='index'), #对于文章列表、标签、类型的处理属于同一界面显示，按照相同逻辑处理
    # 匹配 category/数字/ 形式的路径，捕获 category_id
    path('category/<int:category_id>/', CategoryView.as_view(), name='category-list'),
    # 匹配 tag/数字/ 形式的路径，捕获 tag_id
    path('tag/<int:tag_id>/', TagView.as_view(), name='tag-list'),
    # 匹配 post/数字.html 形式的路径，捕获 post_id
    path('post/<int:post_id>.html', PostDetailView.as_view(), name='post-detail'),
    # 匹配 links/ 路径
    path('links/', links, name='links'),
]
