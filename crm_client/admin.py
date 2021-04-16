from django.contrib import admin

from .models import (
    Departamento,
    Cliente,
    Producto,
    Venta,
    DetalleVenta,
    Proveedor,
    Compra,
    DetalleCompra,
)

admin.site.register(Departamento)
admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Venta)
admin.site.register(DetalleVenta)
admin.site.register(Proveedor)
admin.site.register(Compra)
admin.site.register(DetalleCompra)