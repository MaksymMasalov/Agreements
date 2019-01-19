from django.contrib import admin
from .models import *


class PeriodInline(admin.TabularInline):
   model = Period
   extra = 0


class AgreementAdmin(admin.ModelAdmin):
   list_display = ['negotiator', 'company', 'start_date', 'end_date',
                   'credit', 'debit']
   list_filter = ['negotiator', 'company', 'start_date', 'end_date']
   search_fields = ['start_date', 'end_date']
   inlines = [PeriodInline]

   class Meta:
       model = Agreement


class CountrieAdmin(admin.ModelAdmin):
   list_display = ['code', 'name']
   list_filter = ['code', 'name']
   search_fields = ['code', 'name']

   class Meta:
      model = Countrie


class CompanieAdmin(admin.ModelAdmin):
   list_display = ['name', 'country']
   list_filter = ['name', 'country']
   search_fields = ['name']

   class Meta:
      model = Companie


class PeriodAdmin(admin.ModelAdmin):
   list_display = ['status', 'start_date', 'end_date']
   list_filter = ['status', 'start_date', 'end_date']
   search_fields = ['status', 'start_date', 'end_date']

   class Meta:
      model = Period


admin.site.register(Agreement, AgreementAdmin)
admin.site.register(Countrie, CountrieAdmin)
admin.site.register(Companie, CompanieAdmin)
admin.site.register(Period, PeriodAdmin)
