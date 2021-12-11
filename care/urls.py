"""care URL Configuration

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
from django.urls import path
from django.contrib.auth import views as auth_views

from django.conf.urls.static import static
from django.conf import settings
from accounts.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(),name='logout'),
    path('home/',Home.as_view(), name='home'),


    path('administrator/dashboard/',AdminDashboard.as_view(), name='admin_dashboard'),
    path('administrator/services/',AllServices.as_view(), name='admin_services'),
    path('administrator/services/update/<id>',UpdateService.as_view(), name='update_admin_service'),
    path('administrator/services/delete/<id>',DeleteService.as_view(), name='delete_admin_service'),

    path('provider/signup/',ProviderSignUp.as_view(), name='provider_signup'),
    path('provider/dashboard/',ProviderDashboard.as_view(), name='provider_dashboard'),
    path('provider/services/available/',AvailableServices.as_view(), name='available_services'),
    path('provider/add/service/<id>',AddToMyService.as_view(), name='add_service'),

    path('user/signup/',UserSignup.as_view(), name='user_signup'),
    path('user/dashboard/',UserDashboard.as_view(), name='user_dashboard'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
