"""superlists URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,re_path,include
# from django.conf.urls import include
from lists import urls as list_urls
from lists import views as list_views
#url条目的前半部分是正则表达式，例如'admin/'，定义适用于哪些url。
#后半部分说明把请求发给何处：发给导入的view函数，例如上面的views.home，或者其他的url.py文件，例如blogs.urls

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

# urlpatterns = [re_path(r'^$', list_views.home_page, name='home'),
#                re_path(r'^lists/new$',list_views.new_list,name='new_list'),
#                re_path(r'^lists/(\d+)/$',list_views.view_list,name='view_list'),
#                re_path(r'^lists/(\d+)/add_item$',list_views.add_item,name='add_item'),]

#include可以使用一个正则表达式作为url的前缀，这个前缀会添加到引入的所有url前面
urlpatterns = [re_path(r'^$', list_views.home_page, name='home'),
               re_path(r'^lists/',include(list_urls)),
              ]