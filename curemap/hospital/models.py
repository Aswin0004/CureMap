from django.db import models

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

