""" MAIN URLs """

from django.contrib import admin
from django.urls import path, include
from . import views
from data_loader.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('data_loader/', include('data_loader.urls')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout')
]
