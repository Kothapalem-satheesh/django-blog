

"""blog_main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path, re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from blogs import views as BlogsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('category/', include('blogs.urls')),
    path('blogs/<slug:slug>/', BlogsView.blogs, name='blogs'),
    path('search/', BlogsView.search, name='search'),
    path('subscribe/', BlogsView.register, name='subscribe'),
    path('bookmarks/', BlogsView.my_bookmarks, name='my_bookmarks'),
    path('bookmarks/toggle/<int:blog_id>/', BlogsView.toggle_bookmark, name='toggle_bookmark'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', include('dashboards.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Catch-all — MUST be last. Shows our custom 404 for every unknown URL,
# even when DEBUG=True (where handler404 alone would not fire).
urlpatterns += [re_path(r'^.*$', views.custom_404)]

# Django error handlers (used when DEBUG=False)
handler404 = 'blog_main.views.custom_404'
handler500 = 'blog_main.views.custom_500'
handler403 = 'blog_main.views.custom_403'
handler400 = 'blog_main.views.custom_400'