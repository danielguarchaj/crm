from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated

from .reports import (
    get_all_sales_report,
    get_past_date_range,
)

import datetime

from django.db.models import Count

from django.contrib.auth.models import User

from .models import (
    Cliente,
    Venta,
    Departamento,
)

from .serializers import (
    CustomTokenObtainPairSerializer, 
    ClienteSerializer,
    ClienteSerializerDepth,
    ClienteReportSerializer,
    DepartamentoSerializer,
)

from .filters import (
    ClienteFilter
)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class DepartamentoListAPIView(ListAPIView):
    serializer_class = DepartamentoSerializer
    queryset = Departamento.objects.all()
    permission_classes = [IsAuthenticated]


class ClienteViewSet(ModelViewSet):
    queryset = Cliente.objects.all()
    # permission_classes = [IsAuthenticated]
    filterset_class = ClienteFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return ClienteSerializerDepth
        if self.action == 'retrieve':
            return ClienteReportSerializer
        return ClienteSerializer


class DashboardAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    DAYS_AGO_MONTH = 30
    DAYS_AGO_YEAR = 365
    AGE_RANGES = {
        '15_20': range(15, 21),
        '21_35': range(21, 36),
        '36_50': range(36, 51),
        '51_150': range(51, 151),
    }

    def post(self, request, *args, **kwargs):
        month_range = get_past_date_range(self.DAYS_AGO_MONTH)
        year_range = get_past_date_range(self.DAYS_AGO_YEAR)
        total_clientes = Cliente.objects.count()
        clientes_este_mes = Cliente.objects.filter(fecha_creacion__gte=month_range['after']).count()
        clientes_este_anio = Cliente.objects.filter(fecha_creacion__gte=year_range['after']).count()
        ventas_realizadas = Venta.objects.filter(fecha_creacion__gte=year_range['after']).count()
        clientes_por_departamento = [{
            "departamento": departamento['departamento__nombre'],
            "clientes": departamento['clientes']
        } for departamento in Cliente.objects.values('departamento__nombre').annotate(clientes=Count('id')).order_by('-clientes')]
        clientes_por_edad = self.get_client_age_ranges(Cliente.objects.all())

        ventas_del_anio = get_all_sales_report()

        return Response({
            "total_clientes": total_clientes, 
            "clientes_este_mes": clientes_este_mes, 
            "clientes_este_anio": clientes_este_anio, 
            "ventas_realizadas": ventas_realizadas,
            "clientes_por_departamento": clientes_por_departamento,
            "clientes_por_edad": clientes_por_edad,
            "ventas_del_anio": ventas_del_anio,
        })
    
    def get_client_age_ranges(self, clients):
        result = {
            '15_20': 0,
            '21_35': 0,
            '36_50': 0,
            '51_150': 0,
        }

        for client in clients:
            for age_range in self.AGE_RANGES:
                if client.edad in self.AGE_RANGES[age_range]: 
                    result[age_range] += 1
        
        return result

