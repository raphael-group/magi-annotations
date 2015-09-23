from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def profile(request):
    return render(request, 'accounts/profile.html', context={'user': request.user, 'path': request.path})

def login(request):
    if not request.user.is_authenticated():
        # Automatically send the user to wherever their login
        # request originated. If they don't have a request, just send
        # them to their /account after login
        path = request.GET.get('next')
        path = '/account' if path is None else path
        return render(request, 'accounts/login.html', context={'user': request.user, 'path': path })
    else:
        # If a user is already logged in, send them home
        return redirect('home')
