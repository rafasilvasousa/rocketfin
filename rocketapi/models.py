from django.db import models

# Create your models here.
class Payee(models.Model):
    PAYEE_TYPE_CHOICES = (
        ('C', 'Company'),
        ('P', 'Person'),
    )
    name = models.CharField(max_length=50)
    cpfcnpj = models.CharField(max_length=14)
    payee_type = models.CharField(max_length=1, choices=PAYEE_TYPE_CHOICES)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='payees')
    created_at = models.DateTimeField(auto_now_add=True)

class Account(models.Model):
    bank = models.CharField(max_length=50)
    agency = models.CharField(max_length=50)
    account = models.CharField(max_length=50)
    payee = models.ForeignKey(Payee, on_delete=models.CASCADE, related_name='accounts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bank

class Payment(models.Model):
    STATUS_CHOICES = (
        ('S', 'Scheduled'),
        ('P', 'Paid'),
        ('R', 'Rejected'),
    )
    value = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(default=None, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='S')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    payee = models.ForeignKey(Payee, on_delete=models.CASCADE, related_name='payments')
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    def __str__(self):
        return self.payee.name + ' - ' + str(self.value) + ' - ' + self.status
