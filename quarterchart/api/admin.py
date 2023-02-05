from django.contrib import admin
from .models import Companie, CompanieInfo
# Register your models here.

class CompanieAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": (['name','ticker','market_cap','image_link'])}),
    )

class CompanieInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": (['name','ticker','summary','sector','website','industry'])}),
    )

admin.site.register(Companie, CompanieAdmin)
admin.site.register(CompanieInfo, CompanieInfoAdmin)
        
    
