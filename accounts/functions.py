from .models import *


def AdminCheck(request):
    user = request.user
    if user.is_authenticated:
        try:
            u = Users.objects.get(user=user)
            if u.type == 'admin':
                return (True)
            else:
                return (False)
        except:
            return (False)
    else:
        return (False)

def ProviderCheck(request):
    user = request.user
    if user.is_authenticated:
        try:
            u = Users.objects.get(user=user)
            if u.type == 'service_provider':
                return (True)
            else:
                return (False)
        except:
            return (False)
    else:
        return (False)

def UserCheck(request):
    user = request.user
    if user.is_authenticated:
        try:
            u = Users.objects.get(user=user)
            if u.type == 'public':
                return (True)
            else:
                return (False)
        except:
            return (False)
    else:
        return (False)