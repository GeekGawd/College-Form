from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from form.models import OTP, Registration, StudentForm, User
# Register your models here.

class UserAdmin(BaseUserAdmin):

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    ordering = ['id']
    list_display = ['email','is_superuser']
    list_filter = ['is_active','is_staff', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()

admin.site.register(Registration)
admin.site.register(User, UserAdmin)
admin.site.register(OTP)
admin.site.register(StudentForm)




