from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Account, Payment, Payee
from .serializers import LoginSerializer, AccountSerializer, PaymentSerializer, UserSerializer, PayeeSerializer

# Create your views here.


class LoginViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data
                })
            else:
                return Response({'error': 'Invalid credentials'}, status=401)
        else:
            return Response(serializer.errors, status=400)


class RegisterViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        else:
            return Response(serializer.errors, status=400)


class CheckUsernameViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data['username']
        if User.objects.filter(username=username).exists():
            return Response({'error': 'This username is already in use'}, status=400)
        else:
            return Response({'message': 'This username is available'}, status=200)


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Account.objects.filter(payee__user=user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payee_id = request.data['payee_id']
        user = self.request.user

        try: 
            payee = Payee.objects.get(id=payee_id)
        except Payee.DoesNotExist:
            return Response({'error': 'This payee does not exist'}, status=400)
        
        serializer.save(payee=payee)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


class PayeeViewSet(viewsets.ModelViewSet):
    serializer_class = PayeeSerializer
    permission_classes = [IsAuthenticated]

    # Aqui definimos que o usuário só pode ver os payees que ele mesmo criou, a menos que seja superuser, nesse caso ele pode ver todos os payees
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Payee.objects.all()
        return Payee.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)

        accounts_data = serializer.validated_data.pop('accounts', [])
        cpfcnpj = serializer.validated_data['cpfcnpj']
        user = self.request.user

        if Payee.objects.filter(cpfcnpj=cpfcnpj, user=user).exists():
            return Response({'error': 'This payee is already registered'}, status=400)
        
        self.perform_create(serializer)

        payee = Payee.objects.get(id=serializer.data['id'])
        for account_data in accounts_data:
            existint_account = Account.objects.filter(bank=account_data['bank'], agency=account_data['agency'], account=account_data['account'], payee=payee).exists()
            if not existint_account:
                account = Account.objects.create(payee=payee, **account_data)
                payee.accounts.add(account)
        
        payee_data = PayeeSerializer(payee).data

        headers = self.get_success_headers(serializer.data)
        return Response(payee_data, status=201, headers=headers)


class PaymentViewSet(viewsets.ModelViewSet):
    
    serializer_class = PaymentSerializer

    def get_queryset(self):
        user = self.request.user
        return Payment.objects.filter(user=user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payee_id = request.data['payee']
        account_id = request.data['account']
        user = self.request.user

        payee = Payee.objects.get(id=payee_id)
        if not payee:
            return Response({'error': 'This payee does not exist'}, status=400)
        
        account = Account.objects.get(id=account_id)
        
        serializer.validated_data['user'] = user
        serializer.validated_data['payee'] = payee
        serializer.validated_data['account'] = account
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)