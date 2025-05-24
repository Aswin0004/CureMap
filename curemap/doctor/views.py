from django.shortcuts import render
from .models import Doctor
# Create your views here.


def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor/doctor_list.html', {'doctors': doctors})
