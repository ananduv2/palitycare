from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib.auth.models import User

from django.contrib.auth.forms import PasswordChangeForm
from django.template import RequestContext
import time
import datetime

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
                    return redirect('provider_dashboard')
                elif u.type == 'public':
                    # return HttpResponse("Public")
                    return redirect('user_dashboard')
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
            profile.type='public'
            profile.approval = '1'
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
            profile.type='service_provider'
            profile.approval = '2'
            try:
                profile.save()
            except:
                user.delete()
            return redirect('login')
        else:
            context = {'form': form,'dataform': dataform}
            return render(request,'user/signup.html',context)


class ProviderDashboard(View):
    def get(self, request):
        x = ProviderCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            context = {'account': account}
            return render(request,'provider/dashboard.html',context)
        else:
            return redirect('home')

class UserDashboard(View):
    def get(self, request):
        x = UserCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            context = {'account': account}
            return render(request,'user/dashboard.html',context)
        else:
            return redirect('home')

class AvailableServices(View):
    def get(self, request):
        x = ProviderCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            name = []
            provider_service = ProviderService.objects.filter(user=account)
            for i in provider_service:
                name.append(i.service)
            services = Service.objects.exclude(category__in=name)
            print(services)       
            context = {'account': account, 'services': services}
            return render(request,'provider/available_services.html',context)
        else:
            return redirect('home')

class AddToMyService(View):
    def post(self, request,id):
        x = ProviderCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            service = Service.objects.get(id=id)
            count = request.POST.get('count')
            if count:
                pass
            else:
                count = 1
            cost = request.POST.get('cost')
            ps = ProviderService(user=account,service=service,count=count,cost=cost)
            ps.save()
            return redirect('available_services')
        else:
            return redirect('home')

class MyServices(View):
    def get(self, request):
        x = ProviderCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            ps = ProviderService.objects.filter(user=account)
            sp = SubProduct.objects.filter(service__user=account)
            context = {'account': account,'ps': ps,'sp':sp}
            return render(request,'provider/my_services.html',context)
        else:
            return redirect('home')

class Product(View):
    def get(self,request,id):
        x = ProviderCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            ps = ProviderService.objects.get(id=id)
            sp = SubProduct.objects.filter(service__user=account,service=ps)
            form =  AddSubProductForm()
            context = {'account': account,'ps': ps,'sp':sp,'form': form}
            return render(request,'provider/product.html',context)
        else:
            return redirect('home')

    def post(self, request,id):
        x = ProviderCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            ps = ProviderService.objects.get(id=id)
            sp = SubProduct.objects.filter(service__user=account,service=ps)
            form =  AddSubProductForm(request.POST)
            if form.is_valid:
                f = form.save(commit=False)
                f.service = ps
                if f.count:
                    pass
                else:
                    f.count = 1
                f.save()
                return redirect('product',id=id)
            else:
                context = {'account': account,'ps': ps,'sp':sp,'form': form}
                return render(request,'provider/product.html',context)
        else:
            return redirect('home')

class RemoveService(View):
    def post(self, request,id):
        x = ProviderCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            ps = ProviderService.objects.get(id=id)
            ps.delete()
            return redirect('my_services')
        else:
            return redirect('home')

class RemoveProduct(View):
     def get(self, request,id):
        x = ProviderCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            product = SubProduct.objects.get(id=id)
            service = product.service
            product.delete()
            return redirect('product',id= service.id)
        else:
            return redirect('home')

class PublicService(View):
    def get(self, request):
        x= UserCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            services = ProviderService.objects.all()
            products = SubProduct.objects.all()
            context = {'account': account,'services': services,'products':products}
            return render(request, 'user/services.html',context)


class AddToFavouriteService(View):
    def get(self, request,id):
        x= UserCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            service = ProviderService.objects.get(id=id)
            try:
                fav = UserFavorite.objects.get(user=user,service=service)
                if fav:
                    fav.delete()
                    return redirect('user_services')
                else:
                    fav = UserFavorite(user=account,service=service)
                    fav.save()
                    return redirect('user_services')
            except:
                fav = UserFavorite(user=account,service=service)
                fav.save()
                return redirect('user_services')
        else:
            return redirect('home')

class MyFavorite(View):
    def get(self, request):
        x = UserCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            fs = UserFavorite.objects.filter(user=account)
            context = {'account': account,'fs': fs}
            return render(request,'user/favourite.html',context)
        else:
            return redirect('home')

class WriteReview(View):
    def get(self, request,id):
        x = UserCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            fav = ProviderService.objects.get(id=id)
            form = AddReviewForm()
            context ={'account': account,'form': form}
            return render(request,'user/write_review.html',context)
        else:
            return redirect('home')

    def post(self, request,id):
        x = UserCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            fav = ProviderService.objects.get(id=id)
            form = AddReviewForm(request.POST)
            if form.is_valid:
                f = form.save(commit=False)
                f.user = account
                f.service = fav.service
                f.datetime = datetime.datetime.now()
                f.save()
                return redirect('user_services')
        else:
            return redirect('home')
                
            













            













                




        


        

    

