from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('profile/<int:profile_id>', views.profile, name='profile'),
    
    # path('dashboard', views.dashboard, name='dashboard'),

]
