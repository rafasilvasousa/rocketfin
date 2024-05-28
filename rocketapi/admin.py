from django.contrib import admin
from .models import Payee, Account, Payment

# Register your models here.
@admin.register(Payee)
class PayeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpfcnpj', 'payee_type', 'user', 'created_at')
    list_filter = ('payee_type', 'user')
    search_fields = ('name', 'cpfcnpj')

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('bank', 'agency', 'account', 'payee', 'created_at')
    list_filter = ('bank', 'payee')
    search_fields = ('bank', 'agency', 'account')
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('value', 'payment_date', 'status', 'user', 'payee', 'account', 'created_at')
    list_filter = ('status', 'user', 'payee', 'account')