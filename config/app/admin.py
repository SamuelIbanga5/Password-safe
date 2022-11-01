from django.contrib import admin
from .models import CustomizeUser, PasswordSafe
from django.contrib.auth.admin import UserAdmin

admin.site.register(CustomizeUser, UserAdmin)
admin.site.register(PasswordSafe)