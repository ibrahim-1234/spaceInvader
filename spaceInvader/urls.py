"""spaceInvader URL Configuration

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
from django.urls import path
import userPage.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", userPage.views.home_page, name='home'),
    path("orderList/<order>", userPage.views.order_list, name='orders'),
    path('register/', userPage.views.register_page, name='register'),
    path('login/', userPage.views.login_page,name='login'),
    path('logout', userPage.views.log_out, name='logout'),
    path('users/<name>', userPage.views.user_page, name='users'),
    path('download/', userPage.views.download_file, name='download'),
]
