from datetime import date
from django.db import models
from multiselectfield import MultiSelectField 
from hospital.models import Hospital  # Import Hospital model if in another app





SPECIALIZATION_CHOICES = [
    ('allergy_immunology', 'Allergy & Immunology'),
    ('anesthesiology', 'Anesthesiology'),
    ('audiology', 'Audiology'),
    ('cardiology', 'Cardiology'),
    ('critical_care', 'Critical Care Medicine'),
    ('dermatology', 'Dermatology'),
    ('endocrinology', 'Endocrinology'),
    ('ent', 'ENT (Ear, Nose & Throat)'),
    ('family_medicine', 'Family Medicine'),
    ('gastroenterology', 'Gastroenterology'),
    ('general_medicine', 'General Medicine'),
    ('geriatrics', 'Geriatrics'),
    ('gynecology', 'Gynecology'),
    ('hematology', 'Hematology'),
    ('infectious_diseases', 'Infectious Diseases'),
    ('internal_medicine', 'Internal Medicine'),
    ('nephrology', 'Nephrology'),
    ('neurology', 'Neurology'),
    ('nuclear_medicine', 'Nuclear Medicine'),
    ('obstetrics', 'Obstetrics'),
    ('oncology', 'Oncology'),
    ('ophthalmology', 'Ophthalmology'),
    ('orthopedics', 'Orthopedics'),
    ('pain_management', 'Pain Management'),
    ('pathology', 'Pathology'),
    ('pediatrics', 'Pediatrics'),
    ('plastic_surgery', 'Plastic Surgery'),
    ('psychiatry', 'Psychiatry'),
    ('pulmonology', 'Pulmonology'),
    ('radiology', 'Radiology'),
    ('rheumatology', 'Rheumatology'),
    ('sports_medicine', 'Sports Medicine'),
    ('surgery', 'Surgery'),
    ('urology', 'Urology'),
    ('vascular_surgery', 'Vascular Surgery'),
]


DAY_CHOICES = [
    ('monday', 'Monday'),
    ('tuesday', 'Tuesday'),
    ('wednesday', 'Wednesday'),
    ('thursday', 'Thursday'),
    ('friday', 'Friday'),
    ('saturday', 'Saturday'),
    ('sunday', 'Sunday'),
]
TIME_SLOT_CHOICES = [
    ('09:00 AM', '09:00 AM'),
    ('09:30 AM', '09:30 AM'),
    ('10:00 AM', '10:00 AM'),
    ('10:30 AM', '10:30 AM'),
    ('11:00 AM', '11:00 AM'),
    ('11:30 AM', '11:30 AM'),
    ('12:00 PM', '12:00 PM'),
    ('12:30 PM', '12:30 PM'),
    ('01:00 PM', '01:00 PM'),
    ('01:30 PM', '01:30 PM'),
    ('02:00 PM', '02:00 PM'),
    ('02:30 PM', '02:30 PM'),
    ('03:00 PM', '03:00 PM'),
    ('03:30 PM', '03:30 PM'),
    ('04:00 PM', '04:00 PM'),
    ('04:30 PM', '04:30 PM'),
    ('05:00 PM', '05:00 PM'),
    ('05:30 PM', '05:30 PM'),
    ('06:00 PM', '06:00 PM'),
    ('06:30 PM', '06:30 PM'),
]
class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='doctor_photos/')
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    role = models.CharField(max_length=255, blank=True, null=True)
    qualification = models.TextField(help_text="Use line breaks for paragraphs and * for bullet points.",blank=True, null=True)
    specialization = MultiSelectField(choices=SPECIALIZATION_CHOICES)
    experience_years = models.PositiveIntegerField(blank=True, null=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='doctors')
    available_days = MultiSelectField(choices=DAY_CHOICES, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    rating = models.FloatField(default=0.0)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.first_name} {self.second_name or ''} {self.last_name}".strip()



class DoctorConsultationTimes(models.Model):
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE, related_name='consultation_times')

    monday = MultiSelectField(choices=TIME_SLOT_CHOICES, blank=True,)
    tuesday = MultiSelectField(choices=TIME_SLOT_CHOICES, blank=True)
    wednesday = MultiSelectField(choices=TIME_SLOT_CHOICES, blank=True)
    thursday = MultiSelectField(choices=TIME_SLOT_CHOICES, blank=True)
    friday = MultiSelectField(choices=TIME_SLOT_CHOICES, blank=True)
    saturday = MultiSelectField(choices=TIME_SLOT_CHOICES, blank=True)
    sunday = MultiSelectField(choices=TIME_SLOT_CHOICES, blank=True)

    def __str__(self):
        return f"Consultation Times for Dr. {self.doctor.first_name} {self.doctor.last_name}"




class DoctorBlog(models.Model):
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=255)
    content = models.TextField(help_text="Use line breaks for paragraphs and * for bullet points.")
    image = models.ImageField(upload_to='doctor_blogs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return f"Blogs that made by Dr. {self.doctor.first_name} {self.doctor.last_name}"
    



class DoctorVideo(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    description = models.TextField(help_text="Describe the video content for patients.")
    video_file = models.FileField(upload_to='doctor_videos/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return f"Video by Dr. {self.doctor.first_name} {self.doctor.last_name}: {self.title}"





class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('missed', 'Missed'),
    ]

    # Patient Info
    patient_full_name = models.CharField(max_length=100)
    patient_email = models.EmailField()
    patient_phone = models.CharField(max_length=15)
    patient_age = models.PositiveIntegerField()
    patient_gender = models.CharField(max_length=20)

    # Location Info
    patient_state = models.CharField(max_length=100)
    patient_district = models.CharField(max_length=100)
    patient_place = models.CharField(max_length=100)

    # Foreign Keys (Doctor and Hospital)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='appointments')

    # Appointment Info
    reason = models.TextField()
    appointment_date = models.DateField()
    appointment_time = models.CharField(max_length=20)

    # Whether patient needs an assistant at hospital
    assistant = models.CharField(max_length=3,choices=[('yes', 'Yes'), ('no', 'No')],default='no')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.appointment_date} at {self.appointment_time}"

    def is_past(self):
        return self.appointment_date < date.today()
