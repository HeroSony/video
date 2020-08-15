from django.shortcuts import render, redirect, get_object_or_404
from config import theme
from django.contrib import messages, auth
from django.contrib.auth.models import User
from video.models import Video

def register(request):
    return render(request, theme + '/accounts/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, theme + '/accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')

def profile(request, profile_id):
    profile = get_object_or_404(User, pk=profile_id)
    videos = Video.objects.all()
    if request.user.is_authenticated:
        videos = Video.objects.filter(user=request.user)

    context = {
        'profile': profile,
        'videos': videos
    }
    return render(request, theme + '/accounts/profile.html', context)

# def dashboard(request):
#     return render(request, theme + '/accounts/dashboard.html')
