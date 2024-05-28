from rest_framework import serializers
from .models import Account, Payment, Payee
from django.contrib.auth.models import User
from django.utils import timezone


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use")
        return value
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class AccountSerializer(serializers.ModelSerializer):
    bank = serializers.CharField(required=True)
    agency = serializers.CharField(required=True)
    account = serializers.CharField(required=True)
    class Meta:
        model = Account
        fields = ['id', 'bank', 'agency', 'account']



class PayeeSerializer(serializers.ModelSerializer):
    accounts = AccountSerializer(many=True, required=False)

    class Meta:
        model = Payee
        fields = ['id', 'name', 'cpfcnpj', 'payee_type', 'accounts']
        depth = 1
    
    #Ao criar um payee o usuario podera fornercer uma lista de contas
    def create(self, validated_data):
        user = self.context['request'].user
        payee = Payee.objects.create(user = user, **validated_data)
        return payee
        

class PaymentSerializer(serializers.ModelSerializer):
    value = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_date = serializers.DateField(required=True)
    class Meta:
        model = Payment
        fields = ['id', 'value', 'status', 'payee', 'payment_date', 'account']
        depth = 1

    def validate_payment_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Payment date cannot be in the past")
        return value