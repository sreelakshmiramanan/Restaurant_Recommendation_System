"""restaurantreview URL Configuration

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
from reviewapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('registration', views.registration, name='registration'),
    path('login', views.login, name='login'),
    path('userhome', views.userhome, name='userhome'),
    path('adminhome', views.adminhome, name='adminhome'),
    path('userhotel', views.userhotel, name='userhotel'),
    path('adminhotel', views.adminhotel, name='adminhotel'),
    path('adminrequests', views.adminrequests),
    path('adminuser', views.adminuser, name='adminuser'),
    path('userreview', views.userreview, name='userreview'),
    path('about', views.about, name='about'),
    path('remove', views.remove, name='remove'),
    path('comment', views.comment, name='comment'),
    path('review', views.review, name='review'),
    path('adminhotelview', views.adminhotelview, name='adminhotelview'),
    path('adminhotelreview', views.adminhotelreview, name='adminhotelreview'),
    path('removehotel', views.removehotel, name='removehotel'),
    path('commonhotel', views.commonhotel, name='commonhotel'),
    path('hotelhome', views.hotelhome, name='hotelhome'),
    path('hotelreviews', views.hotelreviews, name='hotelreviews'),
    path('menu', views.menu, name='menu'),
    path('adddish', views.adddish, name='adddish'),
    path('commonmenu', views.commonmenu, name='commonmenu'),
    path('adminmenu', views.adminmenu, name='adminmenu'),
    path('usermenu', views.usermenu, name='usermenu'),
    path('userrequest', views.userrequest),
    path('uservrequest', views.uservrequest),
    path('special', views.special, name='special'),
    path('adspecial', views.adspecial, name='adspecial'),

]
