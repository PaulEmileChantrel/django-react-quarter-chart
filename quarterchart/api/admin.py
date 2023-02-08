from django.contrib import admin
from .models import Companie, CompanieInfo,CompanieBalanceSheet,CompanieCashFlow
# Register your models here.

class CompanieAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": (['name','ticker','market_cap','image_link'])}),
    )

class CompanieInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": (['name','ticker','summary','sector','website','industry'])}),
    )

class CompanieBalanceSheetAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": (['name','ticker','full_annual_unpacked'])}),
    )

class CompanieCashFlowAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": (['name','ticker','full_num_col','full_num_row','light_num_col','light_num_row'])}),)

admin.site.register(Companie, CompanieAdmin)
admin.site.register(CompanieInfo, CompanieInfoAdmin)
admin.site.register(CompanieBalanceSheet, CompanieBalanceSheetAdmin)
admin.site.register(CompanieCashFlow, CompanieCashFlowAdmin)
    
