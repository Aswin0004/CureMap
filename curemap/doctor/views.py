
from django.shortcuts import render, get_object_or_404
from django.shortcuts import get_object_or_404, render
from .models import Doctor
# Create your views here.


def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor/doctor_list.html', {'doctors': doctors})

def doctor_detail(request, doctor_id):
    doctors = get_object_or_404(Doctor, id=doctor_id)
    return render(request, 'doctor/doctor_detail.html', {'doctors': doctors})



