"""
URL configuration for app project.

"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # include the allauth urls
    path('accounts/', include('allauth.urls')),
    # include the home urls
    path('', include('home.urls')),
    path('finance/', include('finance.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)