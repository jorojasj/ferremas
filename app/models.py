from django.db import models

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