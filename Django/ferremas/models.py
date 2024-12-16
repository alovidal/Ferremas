from django.db import models
from django.contrib.auth.models import User

class TipoUsuario(models.Model):
    idTipoUsuario = models.CharField(primary_key=True, db_column="idTipoUsuario", max_length=10)
    descripcion = models.CharField(max_length=100)

    def __str__(self):  
        return f"Tipo de usuario: {self.descripcion}"

class Usuario(models.Model):
    rutUsuario = models.CharField(primary_key=True, max_length=12, db_column="rutUsuario")
    correo = models.OneToOneField(User, on_delete=models.CASCADE)  
    pnombre = models.CharField(max_length=100)
    snombre = models.CharField(max_length=100)
    appaterno = models.CharField(max_length=100)
    apmaterno = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    divisa = models.CharField(max_length=100)
    terminos = models.BooleanField(default=False)
    creacion = models.DateTimeField(auto_now_add=True)
    tipoUsuario = models.ForeignKey("TipoUsuario", on_delete=models.CASCADE, db_column="idTipoUsuario")

    def __str__(self):
        return f"Usuario: {self.pnombre} {self.snombre} {self.appaterno} {self.apmaterno}"


class MarcaProductos(models.Model):
    idMarca = models.CharField(primary_key=True, db_column="idMarca", max_length=10)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return f"Marca del producto: {self.descripcion}"

class CategoriaProductos(models.Model):
    idCategoria = models.CharField(primary_key=True, db_column="idCategoria", max_length=10)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return f"Categoria del producto: {self.descripcion}"

class Producto(models.Model):
    idProducto = models.AutoField(primary_key=True, db_column="idProducto")
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=1000)
    precio = models.FloatField()
    stock = models.IntegerField()
    imagen = models.ImageField(null=True, blank=True)
    marca = models.ForeignKey("MarcaProductos", on_delete=models.CASCADE, db_column="idMarca", max_length=10)
    categoria = models.ForeignKey("CategoriaProductos", on_delete=models.CASCADE, db_column="idCategoria", max_length=10)

    def __str__(self):
            return f"Producto: {str(self.idProducto)+' '+self.nombre}" 
        
    @property
    def imagenURL(self):
        if self.imagen:
            return self.imagen.url  
        return ''
    
class EstadoPedido(models.Model):
    idEstado = models.CharField(primary_key=True, db_column="idEstado", max_length=10)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return f"Estado del pedido: {self.descripcion}"

class Pedido(models.Model):
    idPedido = models.AutoField(primary_key=True, db_column="idPedido")
    usuario = models.ForeignKey("Usuario", on_delete=models.CASCADE, db_column="rutUsuario")
    fecha = models.DateTimeField()
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    correo = models.CharField(max_length=100)
    total = models.FloatField()
    estado = models.ForeignKey("EstadoPedido", on_delete=models.CASCADE, db_column="idEstado")

    def __str__(self):
        return f"Pedido del cliente con rut: {self.usuario.rutUsuario}"
    
class DetallePedido(models.Model):
    idDetalle = models.AutoField(primary_key=True, db_column="idDetalle")
    pedido = models.ForeignKey("Pedido", on_delete=models.CASCADE, db_column="idPedido")
    producto = models.ForeignKey("Producto", on_delete=models.CASCADE, db_column="idProducto")
    cantidad = models.IntegerField()
    total = models.FloatField()

    def __str__(self): 
        return f"Detalle del pedido: {self.pedido} "


class EstadoSolicitudPedido(models.Model):
    idEstadoSolicitud = models.CharField(primary_key=True, db_column="idEstadoSolicitud", max_length=10)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return f"Estado de la solicitud: {self.descripcion}"

class SolicitudPedido(models.Model):
    idSolicitud = models.AutoField(primary_key=True, db_column="idSolicitud")
    usuario = models.ForeignKey("Usuario", on_delete=models.CASCADE, db_column="rutUsuario")
    productos = models.JSONField(null=True, blank=True)
    estado = models.ForeignKey("EstadoSolicitudPedido", on_delete=models.CASCADE, db_column="idEstadoSolicitud")

    def __str__(self):
        return f"Solicitud del usuario con rut: {self.usuario.rutUsuario}"

class EstadoOrden(models.Model):
    idEstadoOrden = models.CharField(primary_key=True, db_column="idEstadoOrden", max_length=10)
    descripcion = models.CharField(max_length=100)

    def __str__(self):  
        return f"Estado de la orden: {self.descripcion}"

class Ordenes(models.Model):
    idOrden = models.AutoField(primary_key=True, db_column="idOrden")
    solicitudPedido = models.ForeignKey("SolicitudPedido", on_delete=models.CASCADE, db_column="idSolicitud")
    estadoOrden = models.ForeignKey("EstadoOrden", on_delete=models.CASCADE, db_column="idEstadoOrden")
    
    def __str__(self):
        return f"Orden del usuario con rut: {self.solicitudPedido.usuario.rutUsuario}"

class TipoInforme(models.Model):
    idTipoInforme = models.CharField(primary_key=True, db_column="idTipoInforme", max_length=10)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return f"Tipo de informe: {self.descripcion}"

class Informe(models.Model):
    idInforme = models.AutoField(primary_key=True, db_column="idInforme")
    usuario = models.ForeignKey("Usuario", on_delete=models.CASCADE, db_column="rutUsuario")
    tipoInforme = models.ForeignKey("TipoInforme", on_delete=models.CASCADE, db_column="idTipoInforme")
    descripcion = models.CharField(max_length=500)
    
    def __str__(self):
        return f"Informe: {self.idInforme} - {self.usuario.rutUsuario}"

class Pagos(models.Model):
    idPago = models.AutoField(primary_key=True, db_column="idPago")
    pedido = models.ForeignKey("Pedido", on_delete=models.CASCADE, db_column="idPedido")
    usuario = models.ForeignKey("Usuario", on_delete=models.CASCADE, db_column="rutUsuario")
    
    def __str__(self):
        return f"Pago del usuario con rut: {self.usuario.rutUsuario}"

class Factura(models.Model):
    idFactura = models.AutoField(primary_key=True, db_column="idFactura")
    usuario = models.ForeignKey("Usuario", on_delete=models.CASCADE, db_column="rutUsuario", null=False, blank=False)
    solicitudPedido =models.ForeignKey ("SolicitudPedido", on_delete=models.CASCADE, db_column="idSolicitud")
    total = models.FloatField()

    def __str__(self):
        return f"Factura del usuario con rut: {self.usuario.rutUsuario}"
    
class Divisas(models.Model):
    idDivisa = models.CharField(primary_key=True, db_column="idDivisa", max_length=10)
    usuario = models.ForeignKey("Usuario", on_delete=models.CASCADE, db_column="rutUsuario")
    descripcion = models.CharField(max_length=100)

    def __str__(self):  
        return f"Divisa del usuario con rut: {self.usuario.rutUsuario}"