from django.contrib import admin
from .models import Link, SideBar
from typeidea_project.base_admin import BaseOwnerAdmin
from typeidea_project.custom_site import custom_site
from typeidea_project.base_admin import BaseOwnerAdmin

# Register your models here.

@admin.register(Link, site=custom_site)
class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'created_time')
    fields = ('title', 'href', 'status', 'weight')
    
    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user #获取当前登录的用户
    #     return super(LinkAdmin, self).save_model(request, obj, form, change)

@admin.register(SideBar, site=custom_site)
class RegisterAdmin(BaseOwnerAdmin):
    list_display = ('title', 'display_type', 'content', 'created_time')
    fields = ('title', 'display_type', 'content')

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user #获取当前登录的用户
    #     return super(RegisterAdmin, self).save_model(request, obj, form, change)