"""
URL configuration for CatFM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers

from apps.catuser.api.viewsets import UserViewSet
from apps.streaming.api.viewsets import StreamingViewSet
from apps.streaming.api.viewsets import PlaylistViewSet
from apps.streaming.api.viewsets import DownloadRequestViewSet
from apps.radio.api.viewsets import RadioStreamViewSet

# Routers
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'streaming', StreamingViewSet)
router.register(r'playlist', PlaylistViewSet)
router.register(r'download_request', DownloadRequestViewSet)
router.register(r'radio_stream', RadioStreamViewSet)

# URLs
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Extra Configs
admin.site.site_header = "CatFM Admin"
admin.site.site_title = "CatFM Admin Portal"
admin.site.index_title = "CatFM Admin Portal"
