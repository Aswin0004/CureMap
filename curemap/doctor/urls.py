from django.urls import path 
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    path('doctor_list/', views.doctor_list,name='doctor_list'),
    path('doctor_detail/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)