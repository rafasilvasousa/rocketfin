from django.core.management.base import BaseCommand
from rocketapi.models import Payment
from django.utils import timezone
class Command(BaseCommand):
    help = 'Update schedulled payments'

    def handle(self, *args, **options):
        today = timezone.now().date()
        schedulled_payments = Payment.objects.filter(
            status= 'S',
            payment_date = today
        )
        for schedulled_payment in schedulled_payments:
            schedulled_payment.status = 'P'
            schedulled_payment.save()
            self.conecta_servico_email(schedulled_payment)

    def conecta_servico_email(self, payment):
        # conecta com o serviço de email para notificar o pagamento
        pass
