from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated

import calendar
import datetime
from dateutil.relativedelta import relativedelta

from django.db.models import Sum, Count, F

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
    permission_classes = [IsAuthenticated]
    filterset_class = ClienteFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ClienteSerializerDepth
        return ClienteSerializer


class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    DAYS_AGO_MONTH = 30
    DAYS_AGO_YEAR = 365
    AGE_RANGES = {
        '15_20': range(15, 21),
        '21_35': range(21, 36),
        '36_50': range(36, 51),
        '51_150': range(51, 151),
    }
    TODAY = datetime.datetime.utcnow()
    MONTHS_AGO_YEAR = 12

    def post(self, request, *args, **kwargs):
        month_range = self.get_past_date_range(self.DAYS_AGO_MONTH)
        year_range = self.get_past_date_range(self.DAYS_AGO_YEAR)
        total_clientes = Cliente.objects.count()
        clientes_este_mes = Cliente.objects.filter(fecha_creacion__gte=month_range['after'], fecha_creacion__lte=month_range['before']).count()
        clientes_este_anio = Cliente.objects.filter(fecha_creacion__gte=year_range['after'], fecha_creacion__lte=year_range['before']).count()
        ventas_realizadas = Venta.objects.filter(fecha_creacion__gte=year_range['after'], fecha_creacion__lte=year_range['before']).count()
        clientes_por_departamento = [{
            "departamento": departamento['departamento__nombre'],
            "clientes": departamento['clientes']
        } for departamento in Cliente.objects.values('departamento__nombre').annotate(clientes=Count('id')).order_by('-clientes')]
        clientes_por_edad = self.get_client_age_ranges(Cliente.objects.all())

        ventas_del_anio = self.get_sales_report()

        return Response({
            "total_clientes": total_clientes, 
            "clientes_este_mes": clientes_este_mes, 
            "clientes_este_anio": clientes_este_anio, 
            "ventas_realizadas": ventas_realizadas,
            "clientes_por_departamento": clientes_por_departamento,
            "clientes_por_edad": clientes_por_edad,
            "ventas_del_anio": ventas_del_anio,
        })
    
    def get_past_date_range(self, past_days):
        delta = datetime.timedelta(days=past_days)
        return {
            "after": self.TODAY - delta,
            "before": self.TODAY
        }
    
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

    def get_sales_report(self):
        last_months = self.get_last_months(self.TODAY, self.MONTHS_AGO_YEAR)
        return [
            {
                "total": Venta.objects.filter(
                                    fecha_creacion__gte=date_range['after'],
                                    fecha_creacion__lte=date_range['before']
                                ).aggregate(total_ventas=Sum('total'))['total_ventas'] or 0,
                "desde": f"{date_range['after'].day}/{date_range['after'].month}/{date_range['after'].year}",
                "hasta": f"{date_range['before'].day}/{date_range['before'].month}/{date_range['before'].year}",
            } for date_range in last_months
        ]
    
    def get_last_months(self, start_date, months):
        for i in range(months):
            yield (self.get_month_range(start_date.year, start_date.month))
            start_date += relativedelta(months = -1)

    def get_month_range(self, year, month):
        first_day = datetime.datetime(year, month, 1)
        last_day = first_day + datetime.timedelta(days=calendar.monthrange(year, month)[1] - 1)
        return {
            "after": first_day,
            "before": last_day,
        }