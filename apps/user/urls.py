"""dailyfresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from django.urls import path, re_path, include
from django.contrib.auth.decorators import login_required
from user.views import register, ActiveView, LoginView, LogoutView, UserInfoView, UserOrderView, AddressView
from user import views
app_name='dailyfresh'

urlpatterns = [
    # path('register', views.register, name='register'), # 注册
    path('register', register.as_view(), name='register'), # 注册
    # path('register_handle', views.register_handle, name='register_handle'), # 注册处理
    re_path(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

    # path('', login_required(UserInfoView.as_view()), name='user'), # 用户中心-信息页
    # path('order', login_required(UserOrderView.as_view()), name='order'), #用户中心-订单页
    # path('address', login_required(AddressView.as_view()), name='address'), # 用户中心-地址页

    path('', UserInfoView.as_view(), name='user'), # 用户中心-信息页
    path('order', UserOrderView.as_view(), name='order'), #用户中心-订单页
    path('address', AddressView.as_view(), name='address'), # 用户中心-地址页

]
