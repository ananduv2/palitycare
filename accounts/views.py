from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib.auth.models import User

from django.contrib.auth.forms import PasswordChangeForm
from django.template import RequestContext

from .models import *
# Create your views here.

class IndexView(View):
    def get(self, request):
        try:
            user = request.user
            context={'user': user}
        except:
            context = {}
        return render(request, 'common/index.html',context)

class LoginView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            # return redirect('home')
            return HttpResponse("Logged In")
        else:
            msg=""
            return render(request,'common/login.html',{'msg':msg})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
            # return HttpResponse("Logged In")
        else:
            msg = "Invalid login credentials"
            return render(request,'common/login.html',{'msg':msg})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class Home(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            try:
                u = Users.objects.get(user=user)
                if u.type == 'admin':
                    # return redirect('admin_dashboard')
                    return HttpResponse("Admin Dashboard")
                elif u.type == 'service_provider':
                    # return HttpResponse("Service Provider")
                    return HttpResponse("Service Provider Dashboard")
                elif u.type == 'public':
                    return HttpResponse("Public")
                else:
                    return redirect('logout')
            except:
                return redirect('logout')
        else:
            return redirect('logout')

