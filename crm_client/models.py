from django.db import models

from django.contrib.auth.models import User

import datetime

ESTADOS = (
    (0, 'Inactivo'),
    (1, 'Activo'),
)

class Departamento(models.Model):
    nombre = models.CharField(max_length=150)

    estado = models.SmallIntegerField(choices=ESTADOS, default=1)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)


class Cliente(models.Model):
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    direccion = models.CharField(max_length=150, blank=True, null=True)
    telefono = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    codigo = models.CharField(max_length=15, blank=True, null=True)
    estado = models.SmallIntegerField(choices=ESTADOS, default=1)
    fecha_creacion = models.DateTimeField()
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    @property
    def edad(self):
        today = datetime.datetime.utcnow()
        today_date = datetime.date(today.year, today.month, today.day)
        birth_date = datetime.date(self.fecha_nacimiento.year, self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        time_difference = today_date - birth_date
        return int(time_difference.days / 365)



class Producto(models.Model):
    codigo = models.CharField(max_length=150)
    nombre = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=150, blank=True, null=True)
    precio_venta = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField()
    fecha_vencimiento = models.DateField(blank=True, null=True)
    estado = models.SmallIntegerField(choices=ESTADOS, default=1)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)


class Venta(models.Model):
    total = models.DecimalField(max_digits=8, decimal_places=2)
    numero_factura = models.CharField(max_length=150)
    comentarios = models.TextField(blank=True, null=True)
    estado = models.SmallIntegerField(choices=ESTADOS, default=1)
    fecha_creacion = models.DateTimeField()
    fecha_modificacion = models.DateTimeField(auto_now=True)

    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)


class DetalleVenta(models.Model):
    cantidad = models.IntegerField()
    precio_venta = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    estado = models.SmallIntegerField(choices=ESTADOS, default=1)
    fecha_creacion = models.DateTimeField()
    fecha_modificacion = models.DateTimeField(auto_now=True)

    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)


class Proveedor(models.Model):
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=150, blank=True, null=True)
    telefono = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    codigo = models.CharField(max_length=15, blank=True, null=True)
    estado = models.SmallIntegerField(choices=ESTADOS, default=1)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)


class Compra(models.Model):
    total = models.DecimalField(max_digits=8, decimal_places=2)
    numero_factura = models.CharField(max_length=150)
    comentarios = models.TextField(blank=True, null=True)
    estado = models.SmallIntegerField(choices=ESTADOS, default=1)
    fecha_creacion = models.DateTimeField()
    fecha_modificacion = models.DateTimeField(auto_now=True)

    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)


class DetalleCompra(models.Model):
    cantidad = models.IntegerField()
    costo_unitario = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    estado = models.SmallIntegerField(choices=ESTADOS, default=1)
    fecha_creacion = models.DateTimeField()
    fecha_modificacion = models.DateTimeField(auto_now=True)

    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)