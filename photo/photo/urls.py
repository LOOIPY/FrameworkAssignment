from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("phones/", include("phoneReview.urls")),


    path("", include("games.urls")),  # 添加 games 应用的 URL
]

# 添加媒体文件的 URL 配置
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
