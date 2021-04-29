from django_filters import rest_framework as filters
from .models import Cliente

class ClienteFilter(filters.FilterSet):
    class Meta:
        model = Cliente
        fields = {
            "nombres": ["icontains"],
            "apellidos": ["icontains"],
            "email": ["icontains"],
            "codigo": ["icontains"],
            "estado": ["exact"],
            "departamento__nombre": ["icontains"],
        }