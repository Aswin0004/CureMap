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
    location_map_url = models.URLField(max_length=2000, blank=True, null=True)
 # Google map location
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
    



# Choice tuples
FEATURE_CHOICES = [
    ('ICU', 'ICU'),
    ('Ambulance', 'Ambulance'),
    ('Pharmacy', 'Pharmacy'),
    ('Blood Bank', 'Blood Bank'),
    ('Operation Theatre', 'Operation Theatre'),
    ('Lab', 'Lab'),
    ('Emergency', 'Emergency'),
    ('Canteen', 'Canteen'),
    ('Parking', 'Parking'),
]

HOSPITAL_TYPE_CHOICES = [
    ('Public', 'Public'),
    ('Private', 'Private'),
    ('Charitable', 'Charitable'),
    ('Specialized', 'Specialized'),
    ('Multi-Specialty', 'Multi-Specialty'),
    ('Teaching', 'Teaching'),
]

INSURANCE_CHOICES = [
    ('Star Health', 'Star Health'),
    ('ICICI Lombard', 'ICICI Lombard'),
    ('Bajaj Allianz', 'Bajaj Allianz'),
    ('Reliance General', 'Reliance General'),
    ('Niva Bupa', 'Niva Bupa'),
    ('Care Health', 'Care Health'),
    ('Aditya Birla', 'Aditya Birla'),
    ('HDFC Ergo', 'HDFC Ergo'),
]
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

class HospitalDetails(models.Model):
    hospital = models.OneToOneField('Hospital', on_delete=models.CASCADE, related_name='details')
    about = models.TextField(help_text="General description about the hospital.Use line breaks for paragraphs and * for bullet points.",blank=True, null=True)
    mission = models.TextField(blank=True, null=True)
    vision = models.TextField(blank=True, null=True)
    features = MultiSelectField(choices=FEATURE_CHOICES, blank=True)
    hospital_type = MultiSelectField(choices=HOSPITAL_TYPE_CHOICES, blank=True)
    insurance_accepted = MultiSelectField(choices=INSURANCE_CHOICES, blank=True)
    specialization = MultiSelectField(choices=SPECIALIZATION_CHOICES, blank=True)
    def __str__(self):
        return f"Details for {self.hospital.name}"