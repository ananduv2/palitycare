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


class UpdateService(View):
    def post(self, request,id):
        x = AdminCheck(request)
        if x == True:
            update_service_name = request.POST.get('update_service_name')
            service = Service.objects.get(id=id)
            service.category = update_service_name
            service.save()
            return redirect('admin_services')
        else:
            return redirect('home')

class DeleteService(View):
    def post(self, request,id):
        x = AdminCheck(request)
        if x == True:
            service = Service.objects.get(id=id)
            service.delete()
            return redirect('admin_services')
        else:
            return redirect('home')

class UserSignup(View):
    def get(self, request):
        form = PublicUserCreationForm()
        dataform = UserSignUpForm()
        context = {'form': form,'dataform': dataform}
        return render(request,'user/signup.html',context)
    
    def post(self, request):
        form = PublicUserCreationForm(request.POST)
        dataform = UserSignUpForm(request.POST)
        if form.is_valid() and dataform.is_valid():
            user = form.save(commit=False)
            user.email = user.username
            user.save()
            profile = dataform.save(commit=False)
            profile.user = user
            profile.email = user.username
            profile.approval = Approved
            try:
                profile.save()
            except:
                user.delete()
            return redirect('login')
        else:
            context = {'form': form,'dataform': dataform}
            return render(request,'user/signup.html',context)


class ProviderSignUp(View):
    def get(self, request):
        form = PublicUserCreationForm()
        dataform = ProviderSignUpForm()
        context = {'form': form,'dataform': dataform}
        return render(request,'provider/signup.html',context)

    def post(self, request):
        form = PublicUserCreationForm(request.POST)
        dataform = UserSignUpForm(request.POST,request.FILES)
        if form.is_valid() and dataform.is_valid():
            user = form.save(commit=False)
            user.email = user.username
            user.save()
            profile = dataform.save(commit=False)
            profile.user = user
            profile.email = user.username
            profile.type='public'
            profile.approval = 'Approved'
            try:
                profile.save()
            except:
                user.delete()
            return redirect('login')
        else:
            context = {'form': form,'dataform': dataform}
            return render(request,'user/signup.html',context)


                




        


        

    

