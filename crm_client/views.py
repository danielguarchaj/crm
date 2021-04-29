from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated

from datetime import date, datetime, timedelta
import calendar

from django.db.models import Sum, Count

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
    def post(self, request, *args, **kwargs):
        current_month_range = self.get_month_range()
        current_year_range = self.get_year_range()
        total_clientes = Cliente.objects.count()
        clientes_este_mes = Cliente.objects.filter(fecha_creacion__gte=current_month_range['after'], fecha_creacion__lte=current_month_range['before']).count()
        clientes_este_anio = Cliente.objects.filter(fecha_creacion__gte=current_year_range['after'], fecha_creacion__lte=current_year_range['before']).count()
        ventas_este_anio = Venta.objects.aggregate(total_ventas=Sum('total'))['total_ventas'] or 0
        clientes_por_departamento = list(Cliente.objects.values('departamento__nombre').annotate(clientes=Count('id')).order_by('-clientes'))

        return Response({
            "total_clientes": total_clientes, 
            "clientes_este_mes": clientes_este_mes, 
            "clientes_este_anio": clientes_este_anio, 
            "ventas_este_anio": ventas_este_anio,
            "clientes_por_departamento": clientes_por_departamento,
        })
    
    def get_month_range(self):
        today = date.today()
        first_day_of_curr_month = datetime(today.year, today.month, 1)
        last_day_of_curr_month = first_day_of_curr_month + timedelta(days=calendar.monthrange(today.year, today.month)[1] - 1)
        return {
            "after": first_day_of_curr_month,
            "before": last_day_of_curr_month
        }
    
    def get_year_range(self):
        today = date.today()
        first_day_of_curr_year = datetime(today.year, 1, 1)
        last_day_of_curr_year = datetime(today.year, 12, 31)
        return {
            "after": first_day_of_curr_year,
            "before": last_day_of_curr_year
        }
    