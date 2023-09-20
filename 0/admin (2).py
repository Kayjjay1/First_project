from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.utils.translation import ugettext_lazy as _

from . import models
# Register your models here.

from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = _('EMR System')

    # Text to put in each page's <h1> (and above login form).
    site_header = _('EMR Managemnent')

    # Text to put at the top of the admin index page.
    index_title = _('EMR administration')

admin_site = CustomAdminSite()
    
class _CustomUserAdmin(UserAdmin):
    model = models.UserModel

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('other_name','dob', 'blood_group', 'genotype', 'phonenumber')}),
    )
    

@admin.register(models.UserModel)
class CustomUserAdmin(_CustomUserAdmin):
    
    registrator_fieldsets = (
        (None, {'fields': ('email', 'phonenumber')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'other_name', 'dob')}),
        (_('Medical info'), {'fields': ( 'blood_group', 'genotype')}),
    )
    
    list_display = ('id', 'first_name', 'last_name', 'other_name')
    
    search_fields = ('first_name', 'other_name', 'last_name')
    
    def change_view(self, request, *args, **kwargs):
        
        # for non-superuser
        if not request.user.is_superuser:
            try:
                self.fieldsets = self.registrator_fieldsets
                response = super(_CustomUserAdmin, self).change_view(request, *args, **kwargs)
            finally:
                # Reset fieldsets to its original value
                self.fieldsets = _CustomUserAdmin.fieldsets
            return response
        else:
            return super(_CustomUserAdmin, self).change_view(request, *args, **kwargs)
