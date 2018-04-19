"""AKblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from user.views import *

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('', include(user.views)),
    path('', index, name='index'),
    path('index/', index, name='index'),
    path('index/<int:page>/', index, name='index'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('user/<str:username>/', user, name='user'),
    path('user/<str:username>/<int:page>/', user, name='user'),
    path('edit/', edit, name='edit'),
    path('popular/', popular, name='popular'),
    path('popular/<int:page>/', popular, name='popular'),
    path('logout/', logout, name='logout'),
    path('follow/', follow, name='follow'),
    path('unfollow/', unfollow, name='unfollow'),
    path('thumbup/', thumbup, name='thumbup'),
    path('post_comment/', post_comment, name='post_comment'),
    path('del_post/', del_post, name='del_post'),
]
