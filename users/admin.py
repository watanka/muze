from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# Register your models here.

# class UserProfileInLine(admin.StackedInline):
#     model = User
#     extra = 1

# class UserAdmin(BaseUserAdmin):
#     inlines = [ UserProfileInLine, ]

# admin.site.unregister(User)
admin.site.register(User)
