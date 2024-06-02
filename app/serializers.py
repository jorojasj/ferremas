from .models import *
from rest_framework import serializers

class ProductoSerializer(serializers.ModelSerializer):
    marca = serializers.CharField(read_only=True, source="marca.nombre_marca")
    class Meta:
        model = Producto
        fields = '__all__'