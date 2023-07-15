from django.contrib import admin
from .models import BankCard


class CardAdmin(admin.ModelAdmin):
    list_display = ('number', 'issue_date', 'exp_date', 'status', 'uuid')
    list_filter = ('issue_date', 'exp_date')


admin.site.register(BankCard, CardAdmin)
