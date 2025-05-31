from django.contrib import admin
from .models import Hospital, HospitalAlbum, HospitalDetails
from django.utils.html import format_html
from multiselectfield import MultiSelectFormField

# Inline admin for hospital album images
class HospitalAlbumInline(admin.TabularInline):
    model = HospitalAlbum
    extra = 1
    can_delete = True
    verbose_name_plural = "Hospital Gallery Images"

# Admin for HospitalDetails
@admin.register(HospitalDetails)
class HospitalDetailsAdmin(admin.ModelAdmin):
    list_display = ('hospital', 'get_features', 'get_types', 'get_insurance')

    def get_features(self, obj):
        return ", ".join(obj.features)
    get_features.short_description = 'Features'

    def get_types(self, obj):
        return ", ".join(obj.hospital_type)
    get_types.short_description = 'Hospital Type'

    def get_insurance(self, obj):
        return ", ".join(obj.insurance_accepted)
    get_insurance.short_description = 'Insurance Accepted'


# Admin for Hospital
@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'contact_number', 'place', 'district', 'state', 'rating', 'open_24_hours')
    search_fields = ('name', 'email', 'place', 'district', 'state')
    list_filter = ('district', 'state', 'open_24_hours')
    exclude = ('password',)
    inlines = [HospitalAlbumInline]  # Inline hospital gallery

# Admin for HospitalAlbum
@admin.register(HospitalAlbum)
class HospitalAlbumAdmin(admin.ModelAdmin):
    list_display = ('hospital', 'image')
