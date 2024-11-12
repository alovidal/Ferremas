# Generated by Django 5.0.6 on 2024-11-12 01:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ferremas', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaProductos',
            fields=[
                ('idCategoria', models.CharField(db_column='idCategoria', max_length=10, primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='EstadoOrden',
            fields=[
                ('idEstadoOrden', models.CharField(db_column='idEstadoOrden', max_length=10, primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='EstadoPedido',
            fields=[
                ('idEstado', models.CharField(db_column='idEstado', max_length=10, primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='EstadoSolicitudPedido',
            fields=[
                ('idEstadoSolicitud', models.CharField(db_column='idEstadoSolicitud', max_length=10, primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MarcaProductos',
            fields=[
                ('idMarca', models.CharField(db_column='idMarca', max_length=10, primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TipoInforme',
            fields=[
                ('idTipoInforme', models.CharField(db_column='idTipoInforme', max_length=10, primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TipoUsuario',
            fields=[
                ('idTipoUsuario', models.CharField(db_column='idTipoUsuario', max_length=10, primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('idPedido', models.AutoField(db_column='idPedido', primary_key=True, serialize=False)),
                ('fecha', models.DateTimeField()),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=20)),
                ('correo', models.CharField(max_length=100)),
                ('total', models.FloatField()),
                ('estado', models.ForeignKey(db_column='idEstado', on_delete=django.db.models.deletion.CASCADE, to='ferremas.estadopedido')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('idProducto', models.AutoField(db_column='idProducto', primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=1000)),
                ('precio', models.FloatField()),
                ('stock', models.IntegerField()),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='')),
                ('categoria', models.ForeignKey(db_column='idCategoria', max_length=10, on_delete=django.db.models.deletion.CASCADE, to='ferremas.categoriaproductos')),
                ('marca', models.ForeignKey(db_column='idMarca', max_length=10, on_delete=django.db.models.deletion.CASCADE, to='ferremas.marcaproductos')),
            ],
        ),
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('idDetalle', models.AutoField(db_column='idDetalle', primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField()),
                ('total', models.FloatField()),
                ('pedido', models.ForeignKey(db_column='idPedido', on_delete=django.db.models.deletion.CASCADE, to='ferremas.pedido')),
                ('producto', models.ForeignKey(db_column='idProducto', on_delete=django.db.models.deletion.CASCADE, to='ferremas.producto')),
            ],
        ),
        migrations.CreateModel(
            name='SolicitudPedido',
            fields=[
                ('idSolicitud', models.AutoField(db_column='idSolicitud', primary_key=True, serialize=False)),
                ('productos', models.JSONField(blank=True, null=True)),
                ('estado', models.ForeignKey(db_column='idEstadoSolicitud', on_delete=django.db.models.deletion.CASCADE, to='ferremas.estadosolicitudpedido')),
            ],
        ),
        migrations.CreateModel(
            name='Ordenes',
            fields=[
                ('idOrden', models.AutoField(db_column='idOrden', primary_key=True, serialize=False)),
                ('estadoOrden', models.ForeignKey(db_column='idEstadoOrden', on_delete=django.db.models.deletion.CASCADE, to='ferremas.estadoorden')),
                ('solicitudPedido', models.ForeignKey(db_column='idSolicitud', on_delete=django.db.models.deletion.CASCADE, to='ferremas.solicitudpedido')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('rutUsuario', models.CharField(db_column='rutUsuario', max_length=12, primary_key=True, serialize=False)),
                ('pnombre', models.CharField(max_length=100)),
                ('snombre', models.CharField(max_length=100)),
                ('appaterno', models.CharField(max_length=100)),
                ('apmaterno', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=20)),
                ('divisa', models.CharField(max_length=100)),
                ('terminos', models.BooleanField(default=False)),
                ('creacion', models.DateTimeField(auto_now_add=True)),
                ('correo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tipoUsuario', models.ForeignKey(db_column='idTipoUsuario', on_delete=django.db.models.deletion.CASCADE, to='ferremas.tipousuario')),
            ],
        ),
        migrations.AddField(
            model_name='solicitudpedido',
            name='usuario',
            field=models.ForeignKey(db_column='rutUsuario', on_delete=django.db.models.deletion.CASCADE, to='ferremas.usuario'),
        ),
        migrations.AddField(
            model_name='pedido',
            name='usuario',
            field=models.ForeignKey(db_column='rutUsuario', on_delete=django.db.models.deletion.CASCADE, to='ferremas.usuario'),
        ),
        migrations.CreateModel(
            name='Pagos',
            fields=[
                ('idPago', models.AutoField(db_column='idPago', primary_key=True, serialize=False)),
                ('pedido', models.ForeignKey(db_column='idPedido', on_delete=django.db.models.deletion.CASCADE, to='ferremas.pedido')),
                ('usuario', models.ForeignKey(db_column='rutUsuario', on_delete=django.db.models.deletion.CASCADE, to='ferremas.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Informe',
            fields=[
                ('idInforme', models.AutoField(db_column='idInforme', primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=500)),
                ('tipoInforme', models.ForeignKey(db_column='idTipoInforme', on_delete=django.db.models.deletion.CASCADE, to='ferremas.tipoinforme')),
                ('usuario', models.ForeignKey(db_column='rutUsuario', on_delete=django.db.models.deletion.CASCADE, to='ferremas.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('idFactura', models.AutoField(db_column='idFactura', primary_key=True, serialize=False)),
                ('total', models.FloatField()),
                ('solicitudPedido', models.ForeignKey(db_column='idSolicitud', on_delete=django.db.models.deletion.CASCADE, to='ferremas.solicitudpedido')),
                ('usuario', models.ForeignKey(db_column='rutUsuario', on_delete=django.db.models.deletion.CASCADE, to='ferremas.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Divisas',
            fields=[
                ('idDivisa', models.CharField(db_column='idDivisa', max_length=10, primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=100)),
                ('usuario', models.ForeignKey(db_column='rutUsuario', on_delete=django.db.models.deletion.CASCADE, to='ferremas.usuario')),
            ],
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
