from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Cliente,
    Departamento,
)

from .reports import (
    get_client_all_sales_report,
    get_client_last_year_sales_report,
    get_client_last_month_sales_report,
)

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user'] = UserSerializer(user).data
        return token


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class ClienteSerializerDepth(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
        depth = 1


class ClienteReportSerializer(serializers.ModelSerializer):
    ventas_acumuladas = serializers.SerializerMethodField()
    ventas_ultimo_anio = serializers.SerializerMethodField()
    ventas_ultimo_mes = serializers.SerializerMethodField()
    class Meta:
        model = Cliente
        fields = '__all__'
        depth = 1
    
    def get_ventas_acumuladas(self, obj):
        return get_client_all_sales_report(obj)
    
    def get_ventas_ultimo_anio(self, obj):
        return get_client_last_year_sales_report(obj)

    def get_ventas_ultimo_mes(self, obj):
        return get_client_last_month_sales_report(obj)


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'