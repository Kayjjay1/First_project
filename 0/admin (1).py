from django.contrib import admin

from hospital.models import DoctorModel, PatientModel
from . import models

# Register your models here.

admin.site.register(PatientModel)

@admin.register(models.PrescriptionModel)
class PrescriptionAdmin(admin.ModelAdmin):
    
    search_fields = ('patient__user__username',)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        
        user = request.user
        
        doctors = DoctorModel.objects.filter(doctor=user)
        
        hospitals = []
        
        for doctor in doctors:
            
            hospitals.append(doctor.hospital)
        
        if db_field.name == "patient":
            
            kwargs["queryset"] = models.PatientModel.objects.filter(hospital__in=hospitals)
            
        if db_field.name == "doctor":
            
            kwargs["queryset"] = models.DoctorModel.objects.filter(doctor=user)
            
        return super().formfield_for_foreignkey(db_field, request, **kwargs)