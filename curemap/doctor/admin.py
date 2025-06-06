from django.contrib import admin
from .models import Doctor, DoctorConsultationTimes, DoctorBlog, DoctorVideo

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'hospital', 'get_specialization', 'is_available')
    search_fields = ('first_name', 'last_name', 'hospital__hospital_name')
    list_filter = ('hospital', 'specialization', 'is_available')

    def get_specialization(self, obj):
        return ", ".join(obj.get_specialization_display())
    get_specialization.short_description = 'Specializations'

@admin.register(DoctorConsultationTimes)
class DoctorConsultationTimesAdmin(admin.ModelAdmin):
    list_display = ('doctor',)

@admin.register(DoctorBlog)
class DoctorBlogAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'title', 'is_published', 'created_at')
    search_fields = ('doctor__first_name', 'doctor__last_name', 'title')
    list_filter = ('is_published', 'created_at')

@admin.register(DoctorVideo)
class DoctorVideoAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'title', 'is_published', 'created_at')
    search_fields = ('doctor__first_name', 'doctor__last_name', 'title')
    list_filter = ('is_published', 'created_at')
