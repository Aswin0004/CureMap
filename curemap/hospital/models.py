from django.db import models
from multiselectfield import MultiSelectField

# Create your models here.

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='hospital_photos/')
    
    email = models.EmailField(blank=True, null=True)
    email2 = models.EmailField(blank=True, null=True)  # Optional second email
    
    contact_number = models.CharField(max_length=15,blank=True, null=True)
    contact_number2 = models.CharField(max_length=15, blank=True, null=True)  # Optional second contact number
    
    password = models.CharField(max_length=128)  # Use Django's default max length for passwords

    website = models.URLField(blank=True, null=True)
    address = models.TextField()
    pincode = models.CharField(max_length=10)
    place = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    location_map_url = models.URLField(blank=True, null=True)  # Google map location
    rating = models.FloatField(default=0.0)

    open_24_hours = models.BooleanField(default=False, help_text="Check if the hospital is open 24 hours")

    def __str__(self):
        return self.name


# models.py
class HospitalAlbum(models.Model):
    hospital = models.ForeignKey('Hospital', on_delete=models.CASCADE, related_name='album')
    image = models.ImageField(upload_to='hospital_gallery/')

    def __str__(self):
        return f"{self.hospital.name} - {self.image.name}"
    



class HospitalDetail(models.Model):
    hospital = models.OneToOneField('Hospital', on_delete=models.CASCADE, related_name='details')

    about = models.TextField(help_text="General description about the hospital.")
    mission = models.TextField(blank=True, null=True)
    vision = models.TextField(blank=True, null=True)

    SPECIALIZATION_CHOICES = [
        ('Cardiology', 'Cardiology'),
        ('Orthopedics', 'Orthopedics'),
        ('Neurology', 'Neurology'),
        ('Pediatrics', 'Pediatrics'),
        ('Oncology', 'Oncology'),
        ('General Surgery', 'General Surgery'),
        ('Gynecology', 'Gynecology'),
        ('Dermatology', 'Dermatology'),
        ('ENT', 'ENT'),
    ]

    SERVICE_CHOICES = [
        ('ICU', 'ICU'),
        ('Emergency', '24/7 Emergency'),
        ('Pharmacy', 'Pharmacy'),
        ('Diagnostics', 'Diagnostics'),
        ('Ambulance', 'Ambulance'),
        ('Blood Bank', 'Blood Bank'),
        ('Physiotherapy', 'Physiotherapy'),
    ]

    FACILITY_CHOICES = [
        ('Parking', 'Parking'),
        ('Canteen', 'Canteen'),
        ('WiFi', 'WiFi'),
        ('Waiting Area', 'Waiting Area'),
        ('ATM', 'ATM'),
        ('Wheelchair Access', 'Wheelchair Access'),
    ]

    specializations = MultiSelectField(choices=SPECIALIZATION_CHOICES, blank=True)
    services = MultiSelectField(choices=SERVICE_CHOICES, blank=True)
    facilities = MultiSelectField(choices=FACILITY_CHOICES, blank=True)

    def __str__(self):
        return f"Details of {self.hospital.name}"

