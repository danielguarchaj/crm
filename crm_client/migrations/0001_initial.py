# Generated by Django 3.2 on 2021-04-16 05:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=150)),
                ('apellidos', models.CharField(max_length=150)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('direccion', models.CharField(blank=True, max_length=150, null=True)),
                ('telefono', models.CharField(blank=True, max_length=150, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('codigo', models.CharField(blank=True, max_length=15, null=True)),
                ('estado', models.SmallIntegerField(choices=[(0, 'Inactivo'), (1, 'Activo')], default=1)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('numero_factura', models.CharField(max_length=150)),
                ('comentarios', models.TextField(blank=True, null=True)),
                ('estado', models.SmallIntegerField(choices=[(0, 'Inactivo'), (1, 'Activo')], default=1)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('estado', models.SmallIntegerField(choices=[(0, 'Inactivo'), (1, 'Activo')], default=1)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=150)),
                ('nombre', models.CharField(max_length=150)),
                ('descripcion', models.CharField(blank=True, max_length=150, null=True)),
                ('precio_venta', models.DecimalField(decimal_places=2, max_digits=8)),
                ('stock', models.IntegerField()),
                ('fecha_vencimiento', models.DateField(blank=True, null=True)),
                ('estado', models.SmallIntegerField(choices=[(0, 'Inactivo'), (1, 'Activo')], default=1)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('direccion', models.CharField(blank=True, max_length=150, null=True)),
                ('telefono', models.CharField(blank=True, max_length=150, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('codigo', models.CharField(blank=True, max_length=15, null=True)),
                ('estado', models.SmallIntegerField(choices=[(0, 'Inactivo'), (1, 'Activo')], default=1)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('numero_factura', models.CharField(max_length=150)),
                ('comentarios', models.TextField(blank=True, null=True)),
                ('estado', models.SmallIntegerField(choices=[(0, 'Inactivo'), (1, 'Activo')], default=1)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_client.cliente')),
                ('vendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('precio_venta', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('estado', models.SmallIntegerField(choices=[(0, 'Inactivo'), (1, 'Activo')], default=1)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_client.producto')),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_client.venta')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleCompra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('costo_unitario', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('estado', models.SmallIntegerField(choices=[(0, 'Inactivo'), (1, 'Activo')], default=1)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_client.compra')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_client.producto')),
            ],
        ),
        migrations.AddField(
            model_name='compra',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_client.proveedor'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='departamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_client.departamento'),
        ),
    ]
