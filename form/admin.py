from django.contrib import admin
from form.models import OTP, Registration, User
# Register your models here.

admin.site.register(Registration)
admin.site.register(User)
admin.site.register(OTP)



