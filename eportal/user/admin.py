from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Enrollment



fields = list(UserAdmin.fieldsets)
fields[1] = ("Personal Info", {"fields": ("first_name", "last_name", "email", "role")})
UserAdmin.fieldsets = tuple(fields)

admin.site.register(CustomUser, UserAdmin)
# Register enrollment
admin.site.register(Enrollment)
