from django.db import models

from django.contrib.auth import get_user_model

# Create your models here.

class HospitalModel(models.Model):

    name = models.CharField(max_length=128)

    location = models.CharField(max_length=256)

    registrator = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="hospitals")
    
    def __str__(self):
        
        return f"{self.name}"
    
    class Meta:
        
        verbose_name = 'Hospital'
        

class DoctorModel(models.Model):

    invite = models.BooleanField(default=True)

    employed = models.BooleanField(default=True)

    status = models.BooleanField(default=False)

    doctor = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)

    hospital = models.ForeignKey(to=HospitalModel, on_delete=models.CASCADE, related_name="doctors")
    
    def __str__(self):
        
        return f"{self.doctor.username}"

    class Meta:

        unique_together = ('doctor', 'hospital')
                
        verbose_name = 'Doctor'
        
        
class PatientModel(models.Model):
    
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="access")
    
    hospital = models.ForeignKey(to=HospitalModel, on_delete=models.CASCADE)
    
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        
        return f"{self.user.username} in {self.hospital.name}"
    
    class Meta:
        
        unique_together = ('user', 'hospital')