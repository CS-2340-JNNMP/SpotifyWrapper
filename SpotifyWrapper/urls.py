"""
URL configuration for SpotifyWrapper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django import views

import accounts
from core.views import index, contact, home
from accounts.views import callback, wrapped_page

urlpatterns = [
    path('index/', index, name='index'),
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path('home/', home, name='home'),
    #path('login/', name='login'),
    # path('registration/', registration, name='sign_up'),
    # path('contact/', contact, name='contact'),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
     #Front end for users
    path('', include('django.contrib.auth.urls')), #back end auth
    path('accounts/', include('accounts.urls')),
    path('spotify/', include('accounts.urls')),

    path('spotify/callback/wrapped-page', wrapped_page, name='wrapped_page'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)