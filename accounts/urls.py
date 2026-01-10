from django.urls import path
from . import views

urlpatterns = [
    # Google OAuth endpoints
    path('google/', views.GoogleLogin.as_view(), name='google_login'),
    path('google/redirect/', views.google_login_redirect, name='google_login_redirect'),
    path('google/callback/', views.google_callback, name='google_callback'),
    
    # User endpoints
    path('user/', views.user_profile, name='user_profile'),
    path('logout/', views.logout_view, name='logout'),
]
