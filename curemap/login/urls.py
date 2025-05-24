from django.urls import path # type: ignore
from . import views


urlpatterns = [

    path('login_user/', views.login_user,name='login_user'),
    path('register_user/', views.register_user,name='register_user'),
    path('logout/', views.logout_user, name='logout_user'),
]