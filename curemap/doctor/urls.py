from django.urls import path 
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    path('doctor_list/', views.doctor_list,name='doctor_list'),
    # path('hospital/<int:hospital_id>/', views.hospital_detail, name='hospital_detail'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)