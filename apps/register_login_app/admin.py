from django.contrib import admin
from .models import CustomUser

class CustomerUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(CustomUser, CustomerUserAdmin)