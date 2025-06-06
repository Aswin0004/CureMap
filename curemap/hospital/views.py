from django.shortcuts import render, get_object_or_404
from .models import Hospital,HospitalAlbum
from doctor.models import Doctor 


# Create your views here.
def hospital_list(request):
    hospitals = Hospital.objects.all()
    return render(request, 'hospital/hospital_list.html', {'hospitals': hospitals})




def hospital_detail(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    doctors = hospital.doctors.all()
    return render(request, 'hospital/hospital_detail.html', {'hospital': hospital,'hospitals':hospital,'doctors': doctors,})