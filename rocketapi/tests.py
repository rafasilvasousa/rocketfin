from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rocketapi.models import Payee, Account, Payment


# Create your tests here.
class LoginViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = '/login/'
        self.username = 'root'
        self.password = 'r0cketf!n'
        self.user = User.objects.create_user(username=self.username, password=self.password)
    
    
    def test_login_with_valid_credentials(self):
        response = self.client.post(self.login_url, {'username': self.username, 'password': self.password}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('access' in response.data)
        self.assertTrue('user' in response.data)

    def test_login_with_invalid_credentials(self):
        response = self.client.post(self.login_url, {'username': 'rafael', 'password': 'invalid'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue('error' in response.data)
        self.assertNotIn('access', response.data)
        self.assertNotIn('user', response.data)

class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/register/'
        self.username = 'rafael'
        self.password = 'r4f43l'
        self.first_name = 'Rafael'
        self.last_name = 'Henrique'
        self.email = 'rafael@tananan.com'

        self.username_fail = 'rafael1'
        self.password_fail = 'r4f43l1'
        self.first_name_fail = 'Rafael1'
        self.last_name_fail = 'Henrique1'
        self.email_fail = 'rafael1@tananan.com'
        self.user = User.objects.create_user(username=self.username_fail, password=self.password_fail, first_name=self.first_name_fail, last_name=self.last_name_fail, email=self.email_fail)

    def test_register_with_valid_data(self):
        response = self.client.post(self.register_url, {'username': self.username, 'password': self.password, 'first_name': self.first_name, 'last_name': self.last_name, 'email': self.email}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('access' in response.data)
        self.assertTrue('user' in response.data)

    def test_register_with_invalid_data(self):
        response = self.client.post(self.register_url, {'username': self.username_fail, 'password': self.password_fail, 'first_name': self.first_name_fail, 'last_name': self.last_name_fail, 'email': self.email_fail}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('access', response.data)
        self.assertNotIn('user', response.data)

class CheckUsernameViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.check_username_url = '/check-username/'
        self.username = 'rafael'
        self.password = 'r4f43l'
        self.first_name = 'Rafael'
        self.last_name = 'Henrique'
        self.email = 'rafael@tananan.com'
        self.user = User.objects.create_user(username=self.username, password=self.password, first_name=self.first_name, last_name=self.last_name, email=self.email)

    def test_check_username_with_valid_data(self):
        response = self.client.post(self.check_username_url, {'username': 'rafael1'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in response.data)
        self.assertNotIn('error', response.data)

    def test_check_username_with_invalid_data(self):
        response = self.client.post(self.check_username_url, {'username': 'rafael'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('error' in response.data)
        self.assertNotIn('message', response.data)

class PayeeViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='rafaelteste', password='r4f43l', first_name='Rafael', last_name='Henrique', email='rafa@lala.com')
        self.token = RefreshToken.for_user(self.user).access_token
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.payee_url = '/payees/'

    #Cria um beneficiario sem dados de conta
    def test_create_payee(self):
        response = self.client.post(self.payee_url, {'name': 'Rafael', 'cpfcnpj': '12345678901', 'payee_type': 'P'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue('id' in response.data)
        self.assertTrue('name' in response.data)
        self.assertTrue('cpfcnpj' in response.data)
        self.assertTrue('payee_type' in response.data)
        self.assertTrue('accounts' in response.data)
    
    def test_create_payee_with_account(self):
        response = self.client.post(self.payee_url, {'name': 'Rafael', 'cpfcnpj': '12345678901', 'payee_type': 'P', 'accounts': [{'bank': 'Nubank', 'agency': '0001', 'account': '123456'}]}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue('id' in response.data)
        self.assertTrue('name' in response.data)
        self.assertTrue('cpfcnpj' in response.data)
        self.assertTrue('payee_type' in response.data)
        self.assertTrue('accounts' in response.data)



    def test_create_duplicated_payee(self):
        response = self.client.post(self.payee_url, {'name': 'Rafael', 'cpfcnpj': '12345678901', 'payee_type': 'P'}, format='json')
        response2 = self.client.post(self.payee_url, {'name': 'Rafael', 'cpfcnpj': '12345678901', 'payee_type': 'P'}, format='json')
        self.assertEqual(response2.status_code, 400)
        self.assertTrue('error' in response2.data)

class AccountViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='rafaelteste', password='r4f43l', first_name='Rafael', last_name='Henrique',
        email='raa@tanana.com')
        self.token = RefreshToken.for_user(self.user).access_token
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.account_url = '/accounts/'
        self.payee_url = '/payees/'
        self.payee = Payee.objects.create(name='Rafael', cpfcnpj='12345678901', payee_type='P', user=self.user)
        self.payee_id = self.payee.id

    def test_create_account(self):
        response = self.client.post(self.account_url, {'bank': 'Nubank', 'agency': '0001', 'account': '123456', 'payee_id': self.payee_id}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue('id' in response.data)

class PaymentViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='rafaelteste', password='r4f43l', first_name='Rafael', last_name='Henrique', email='rafa@tanana.com')
        self.token = RefreshToken.for_user(self.user).access_token
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.payment_url = '/payments/'
        self.payee = Payee.objects.create(name='Rafael', cpfcnpj='12345678901', payee_type='P', user=self.user)
        self.payee_id = self.payee.id
        self.account = Account.objects.create(bank='Nubank', agency='0001', account='123', payee=self.payee)
        self.account_id = self.account.id

    def test_create_payment(self):
        response = self.client.post(self.payment_url, {'value': 100.00, 'status': 'S', 'payee': self.payee_id, 'payment_date':'2024-05-28', 'account': self.account_id}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue('id' in response.data)

    def teste_create_payment_with_invalid_data(self):
        response = self.client.post(self.payment_url, {'value': 100.00, 'status': 'S', 'payee': self.payee_id, 'payment_date':'2022-05-10', 'account': self.account_id}, format='json')
        self.assertEqual(response.status_code, 400)

class PayeeListTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='rafaelteste', password='r4f43l', first_name='Rafael', last_name='Henrique', email='r@tanana.com')
        self.token = RefreshToken.for_user(self.user).access_token
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.payee_url = '/payees/'
        Payee.objects.create(name='Rafael', cpfcnpj='12345678901', payee_type='P', user=self.user)
        Payee.objects.create(name='Henrique', cpfcnpj='12345678901', payee_type='P', user=self.user)
        Payee.objects.create(name='Rafael Henrique', cpfcnpj='123456789', payee_type='P', user=self.user)

    def test_list_payees(self):
        response = self.client.get(self.payee_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

class AccountListTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='rafaelteste', password='r4f43l', first_name='Rafael', last_name='Henrique', email='r@tananan.com')
        self.token = RefreshToken.for_user(self.user).access_token
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.account_url = '/accounts/'
        payee = Payee.objects.create(name='Rafael', cpfcnpj='12345678901', payee_type='P', user=self.user)
        Account.objects.create(bank='Nubank', agency='000', account='123', payee=payee)
        Account.objects.create(bank='Itau', agency='000', account='123', payee=payee)
        Account.objects.create(bank='Bradesco', agency='000', account='123', payee=payee)
                               
    def test_list_accounts(self):
        response = self.client.get(self.account_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

class PaymentListTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='rafaelteste', password='r4f43l', first_name='Rafael', last_name='Henrique', email='r@tananan.com')
        self.token = RefreshToken.for_user(self.user).access_token
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.payment_url = '/payments/'
        payee = Payee.objects.create(name='Rafael', cpfcnpj='12345678901', payee_type='P', user=self.user)
        account = Account.objects.create(bank='Nubank', agency='000', account='123', payee=payee)
        Payment.objects.create(value=100.00, status='S', payee=payee, payment_date='2024-05-28', account=account, user=self.user)
        Payment.objects.create(value=100.00, status='S', payee=payee, payment_date='2024-05-28', account=account, user=self.user)
        Payment.objects.create(value=100.00, status='S', payee=payee, payment_date='2024-05-28', account=account, user=self.user)

    def test_list_payments(self):
        response = self.client.get(self.payment_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

class UpdatePaymentStatusTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='rafaelteste', password='r4f43l', first_name='Rafael', last_name='Henrique', email='r@tananan.com')
        self.token = RefreshToken.for_user(self.user).access_token
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.payment_url = '/payments/'
        payee = Payee.objects.create(name='Rafael', cpfcnpj='12345678901', payee_type='P', user=self.user)
        account = Account.objects.create(bank='Nubank', agency='000', account='123', payee=payee)
        self.payment = Payment.objects.create(value=100.00, status='S', payee=payee, payment_date='2024-05-28', account=account, user=self.user)
        self.payment_id = self.payment.id

    def test_update_payment_status(self):
        response = self.client.patch(self.payment_url, {'payment_id': self.payment_id, 'status': 'P'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('status' in response.data, True)
                                             