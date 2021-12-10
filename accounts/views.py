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
from .functions import *
from .forms import *
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
                    return redirect('admin_dashboard')
                    # return HttpResponse("Admin Dashboard")
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


class AdminDashboard(View):
    def get(self, request):
        x = AdminCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            providers = Users.objects.filter(type='service_provider').count()
            public = Users.objects.filter(type='public').count()
            services = Service.objects.all().count()
            context = {'account': account,'providers': providers,'public': public,'services': services}
            return render(request, 'admin/dashboard.html', context)
        else:
            return redirect('home')

class AllServices(View):
    def get(self, request):
        x = AdminCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            services = Service.objects.all()
            form = AddServiceForm()
            context = {'account':account,'services':services,'form':form}
            return render(request, 'admin/services.html', context)
        else:
            return redirect('home')

    def post(self, request):
        x = AdminCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            services = Service.objects.all()
            form = AddServiceForm(request.POST)
            if form.is_valid:
                f = form.save(commit=False)
                f.providers = 0
                f.users = 0
                f.save()
                return redirect('admin_services')
            else:
                alert="Adding service failed."
                context = {'account':account,'services':services,'form':form}
                return render(request, 'admin/services.html', context)
        else:
            return redirect('home')
        


        

    

