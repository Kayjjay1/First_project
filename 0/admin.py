from django.contrib import admin

# Register your models here.

from . import models


@admin.register(models.HospitalModel)
class HospitalAdmin(admin.ModelAdmin):

    list_display = ('name', 'location', 'registrator')


@admin.register(models.DoctorModel)
class DoctorAdmin(admin.ModelAdmin):

    list_display = ( 'doctor', 'invite', 'status', 'hospital', 'employed')