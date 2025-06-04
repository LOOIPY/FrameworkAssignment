# app/admin.py

from django.contrib import admin
from .models import Property, PropertyImage

class PropertyImageInline(admin.TabularInline):
    """
    在 Property 后台编辑页面以表格形式显示 PropertyImage。
    extra = 2 表示默认空出 2 个可上传图片的行。
    """
    model = PropertyImage
    extra = 2

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price')
    inlines = [PropertyImageInline]
    # 这样在 Property 后台页面就能看到一个“PropertyImage”表格，方便上传多张细节图

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'caption', 'image')

