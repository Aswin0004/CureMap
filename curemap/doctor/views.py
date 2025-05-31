<<<<<<< HEAD
from django.shortcuts import render, get_object_or_404
=======
from django.shortcuts import get_object_or_404, render
>>>>>>> 9e9b906 (doctor and hospital model change commit)
from .models import Doctor
# Create your views here.


def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor/doctor_list.html', {'doctors': doctors})

<<<<<<< HEAD
def doctor_detail(request, doctor_id):
    doctors = get_object_or_404(Doctor, id=doctor_id)
    return render(request, 'doctor/doctor_detail.html', {'doctors': doctors})
=======




def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, 'doctor/doctor_detail.html', {'doctor': doctor,})
>>>>>>> 9e9b906 (doctor and hospital model change commit)
