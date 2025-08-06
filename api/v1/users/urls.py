from django.urls import path
from .views import RegisterView, LoginView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('registrations/',RegisterView.as_view() , name = 'Register'),
    path('login/',LoginView.as_view(), name = 'User Login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/',LogoutView.as_view(), name='User Logout')
    
]