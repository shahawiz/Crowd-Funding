"""kickpro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,include
from project.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls import url



urlpatterns = [
    path('admin/', admin.site.urls),
    path('project/',include('project.urls')),
    path('',home,name='home'),
    path('register/',register,name='register'),
    path('user/myprofile',UserProfile,name='user_profile'),
    path('user/<int:user_id>/',publicProfile,name='user_PublicProfile'),
    path('search/<slug:searchText>/',search,name='search'),
    path('discover',Discover,name='discover'),
    path('login/',user_login,name='login'),
    path('sign_up/',register,name='sign_up'),
    path('index/',index,name='index'),
    path('logout/',auth_views.LogoutView.as_view(template_name='home.html'),name='logout'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),


]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
