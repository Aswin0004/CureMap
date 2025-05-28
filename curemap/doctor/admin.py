from django.contrib import admin
<<<<<<< HEAD
from .models import Doctor,Blog,Doctor_consultation_times
=======
from .models import Doctor,DoctorBlog,DoctorConsultationTimes
>>>>>>> 957636e (doctor and hospital model update)
# Register your models here.

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'second_name', 'last_name', 'hospital',
        'specialization_display', 'experience_years', 'is_available', 'rating'
    )
    list_filter = ('hospital', 'specialization', 'available_days', 'is_available')
    search_fields = ('first_name', 'second_name', 'last_name', 'email', 'hospital__name')
    readonly_fields = ('rating',)

    def specialization_display(self, obj):
        return ", ".join(obj.specialization)
    specialization_display.short_description = 'Specializations'


<<<<<<< HEAD
admin.site.register(Blog)
admin.site.register(Doctor_consultation_times)
=======



admin.site.register(DoctorBlog)
admin.site.register(DoctorConsultationTimes)
>>>>>>> 957636e (doctor and hospital model update)
