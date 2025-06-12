
from datetime import date
from django.shortcuts import render, get_object_or_404
from django.shortcuts import get_object_or_404, render
from .models import Doctor,DoctorConsultationTimes
from django.http import JsonResponse
from hospital.models import Hospital
from user.models import UserProfile 
# Create your views here.


def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor/doctor_list.html', {'doctors': doctors})


# Doctor Detail View
def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    hospitals = Hospital.objects.all()
    return render(request, 'doctor/doctor_detail.html', {
        'doctor': doctor,
        'hospitals': hospitals
    })

# Appointment Form View
def appointment(request):
    user = request.user

    context = {
        'doctors': Doctor.objects.all(),
        'hospitals': Hospital.objects.all(),
    }
    return render(request, 'appointment/appointment_form.html', context)