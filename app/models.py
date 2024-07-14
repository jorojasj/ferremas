from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Marca(models.Model):
    id_marca = models.IntegerField(primary_key=True)
    nombre_marca = models.CharField(max_length=30, null=False)

    def __str__(self):
        txt = "Id: {0} - Nombre: {1}"
        return txt.format(self.id_marca, self.nombre_marca)

class Categoria(models.Model):
    id_categoria = models.IntegerField(primary_key=True)
    nombre_categoria = models.CharField(max_length=30, null=False)

    def __str__(self):
        txt = "Id: {0} - Nombre: {1}"
        return txt.format(self.id_categoria, self.nombre_categoria)
    
class Producto(models.Model):
    id_producto = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=40, null=False)
    precio = models.IntegerField(null=False)
    stock  = models.IntegerField(null=False)
    descripcion = models.CharField(max_length=100, null=False)
    imagen = models.ImageField(upload_to='imagenesProducto')
    fecha_agregar = models.DateField(auto_now_add=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        txt = "Codigo: {0} - Nombre: {1} - Stock: {2}"
        return txt.format(self.id_producto, self.nombre, self.stock)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=0, default=0.00)

    def save(self, *args, **kwargs):
        self.subtotal = self.producto.precio * self.cantidad
        super().save(*args, **kwargs)

class Pedido(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='pendiente')
    metodo_entrega = models.CharField(max_length=20, default='tienda')
    metodo_pago = models.CharField(max_length=20, default='debito')
    total = models.DecimalField(max_digits=10, decimal_places=0, default=0.00)

    def __str__(self):
        return f"Pedido {self.id} - Cliente: {self.cliente.username}"
    
class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle {self.id} - Pedido: {self.pedido.id}"
    
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20)

    def __str__(self):
        return f"Perfil de {self.usuario.username} - Rol: {self.rol}"

class Pago(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name='pago')
    confirmado = models.BooleanField(default=False)
    fecha_pago = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Pago - Pedido: {self.pedido.id} - Confirmado: {self.confirmado}"