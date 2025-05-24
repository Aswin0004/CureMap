from django.contrib import admin
from .models import Hospital ,HospitalAlbum # Adjust the import path if needed

from django.utils.html import format_html
# Register your models here.
# Define inline for HospitalAlbum

@admin.register(HospitalAlbum)
class HospitalAlbumAdmin(admin.ModelAdmin):
    list_display = ('hospital', 'image')

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'contact_number', 'place', 'district', 'state', 'rating', 'open_24_hours')
    search_fields = ('name', 'email', 'place', 'district', 'state')
    list_filter = ('district', 'state', 'open_24_hours')
    exclude = ('password',)
 # or use readonly_fields if you want to show but not allow edits

e = True  # Allow deleting album images
