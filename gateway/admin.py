from django.contrib import admin
from .models import TenantConfig

# Register your models here.
class TenantConfigAdmin(admin.ModelAdmin):
    pass

admin.site.register(TenantConfig, TenantConfigAdmin)
