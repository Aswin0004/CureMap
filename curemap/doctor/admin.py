from django.contrib import admin
from .models import Doctor,DoctorConsultationTimes,DoctorBlog
from .models import Doctor,DoctorBlog,DoctorConsultationTimes
# Register your models here.

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'second_name', 'last_name', 'role', 'hospital',
        'specialization_display', 'experience_years', 'is_available', 'rating'
    )
    list_filter = ('hospital', 'specialization', 'available_days', 'is_available')
    search_fields = ('first_name', 'second_name', 'last_name', 'email', 'hospital__name')
    readonly_fields = ('rating',)

    def specialization_display(self, obj):
        return ", ".join(obj.specialization)
    specialization_display.short_description = 'Specializations'



admin.site.register(DoctorBlog)
admin.site.register(DoctorConsultationTimes)
