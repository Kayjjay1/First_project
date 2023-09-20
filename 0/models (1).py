from django.db import models
from hospital.models import DoctorModel, PatientModel

# Create your models here.

class PrescriptionModel(models.Model):

    doctor = models.ForeignKey(to=DoctorModel, on_delete=models.CASCADE)

    patient = models.ForeignKey(to=PatientModel, on_delete=models.CASCADE)

    medication = models.TextField(max_length=256)

    dispensation_instruction = models.TextField(max_length=256)

    patient_instrution = models.TextField(max_length=256)

    complaint = models.TextField(max_length=512)
    
    class Meta:
        
        verbose_name = 'Prescription'