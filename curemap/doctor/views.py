
from datetime import date, datetime
from django.shortcuts import redirect, render, get_object_or_404
from django.shortcuts import get_object_or_404, render
from .models import Doctor,DoctorConsultationTimes,Appointment
from django.http import JsonResponse
from hospital.models import Hospital
from user.models import UserProfile 
# Create your views here.


def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor/doctor_list.html', {'doctors': doctors})


# Doctor Detail View
def doctor_detail(request, doctor_id):
    user = request.user
    profile = getattr(user, 'userprofile', None)
    doctor = get_object_or_404(Doctor, id=doctor_id)

    # Age Calculation
    age = None
    if profile and profile.dob:
        today = datetime.today().date()
        age = today.year - profile.dob.year - ((today.month, today.day) < (profile.dob.month, profile.dob.day))

    if request.method == 'POST':
        selected_doctor_id = request.POST.get('consulting_doctor')
        doctor = get_object_or_404(Doctor, id=selected_doctor_id)


        hospital_id = request.POST.get('hospital')
        hospital = get_object_or_404(Hospital, id=hospital_id)

        Appointment.objects.create(
            patient_full_name=request.POST.get('patient_full_name'),
            patient_email=request.POST.get('patient_email'),
            patient_phone=request.POST.get('patient_phone'),
            patient_age=request.POST.get('patient_age'),
            patient_gender=request.POST.get('patient_gender'),
            patient_state=request.POST.get('patient_state'),
            patient_district=request.POST.get('patient_district'),
            patient_place=request.POST.get('patient_place'),
            doctor=doctor,
            hospital=hospital,
            reason=request.POST.get('reason'),
            assistant=request.POST.get('assistant'),
            appointment_date=request.POST.get('appointment_date'),
            appointment_time=request.POST.get('appointment_time'),
        )
        return redirect('doctor_detail', doctor_id=doctor.id)


    return render(request, 'doctor/doctor_detail.html', {
        'profile': profile,
        'doctor': doctor,
        'doctors': Doctor.objects.all(),
        'hospitals': Hospital.objects.all(),
        'age': age,
    })

# Appointment Form View
def appointment(request):
    user = request.user

    context = {
        'doctors': Doctor.objects.all(),
        'hospitals': Hospital.objects.all(),
    }
    return render(request, 'appointment/appointment_form.html', context)