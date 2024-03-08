from django.urls import path
from .views import create_reminder,user_login,user_logout

urlpatterns = [
    path('user-login',user_login),
    path('user-logout', user_logout),
    path('create-reminder',create_reminder),
]
