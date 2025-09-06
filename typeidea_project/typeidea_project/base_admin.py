from django.contrib import admin

class BaseOwnerAdmin(admin.ModelAdmin):
    """
    1. 用来自动补充文章、分类、标签、侧边栏、友链这是Model的owner字段
    2. 用来针对queryset过滤当前用户的数据
    """

    exclude = ('owner', )
    #设置不同后台管理员对于各自管理内容的可见性
    def get_queryset(self, request):
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)
    #设置用户对于blog各项设置的权限
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)