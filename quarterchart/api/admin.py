from django.contrib import admin
from .models import Companie, CompanieInfo,CompanieBalanceSheet,CompanieCashFlow, CompanieIncomeStatement,Currency
# Register your models here.

class CompanieAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": (['name','ticker','market_cap','image_link','data_was_downloaded'])}),
    )

class CompanieInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": (['name','ticker','summary','sector','website','industry','next_earnings_date'])}),
    )

class CompanieBalanceSheetAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": (['name','ticker','full_num_col','full_num_row','light_num_col','light_num_row'])}),)


class CompanieCashFlowAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": (['name','ticker','full_num_col','full_num_row','light_num_col','light_num_row'])}),)

class CompanieIncomeStatementAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": (['name','ticker','full_num_col','full_num_row','light_num_col','light_num_row'])}),)

class CurrencyAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": (['name','ticker','last_updated_at','value'])}),
    )
admin.site.register(Companie, CompanieAdmin)
admin.site.register(CompanieInfo, CompanieInfoAdmin)
admin.site.register(CompanieBalanceSheet, CompanieBalanceSheetAdmin)
admin.site.register(CompanieCashFlow, CompanieCashFlowAdmin)
admin.site.register(CompanieIncomeStatement, CompanieIncomeStatementAdmin)
admin.site.register(Currency, CurrencyAdmin)