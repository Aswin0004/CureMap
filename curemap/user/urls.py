from django.urls import path 
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    path('', views.homepage,name='homepage'),
    path('user_profile/', views.user_profile,name='user_profile'),
    path('edit_user_profile/', views.edit_user_profile, name='edit_user_profile'),
    path('add_family_member/', views.add_family_member, name='add_family_member'),




# ADMIN PAGE 


    path('super_admin/', views.super_admin,name='super_admin'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)