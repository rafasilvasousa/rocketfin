import django_filters
from .models import Payment, Account, Payee


class PaymentFilter(django_filters.FilterSet):
    class Meta:
        model = Payment
        fields = {
            'status': ['exact'],
            'payment_date': ['exact', 'lt', 'gt'],
            'payee': ['exact'],
            
        }

class PayeeFilter(django_filters.FilterSet):
    class Meta:
        model = Payee
        fields = {
            'name': ['exact'],
            'cpfcnpj': ['exact'],
            'payee_type': ['exact'],
        }

class AccountFilter(django_filters.FilterSet):
    class Meta:
        model = Account
        fields = {
            'bank': ['exact'],
            'agency': ['exact'],
            'account': ['exact'],
            'payee': ['exact'],
        }