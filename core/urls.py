from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home and authentication
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Room management
    path('rooms/', views.room_status, name='room_status'),
    
    # Guest management
    path('guests/', views.guest_list, name='guest_list'),
    path('check-in/', views.check_in_guest, name='check_in_guest'),
    path('check-out/<int:guest_id>/', views.check_out_guest, name='check_out_guest'),
]
