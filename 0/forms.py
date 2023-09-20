from . import models

from django import forms

class UserForm(forms.ModelForm):

    class Meta:
        
        model = models.UserModel
        
        exclude = ['first_name', 'last_name', 'other_name', 'dob', 'password', 'username', 'genotype', 'blood_group', 'phone_numbers']