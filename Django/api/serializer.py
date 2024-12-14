from rest_framework import serializers
from ferremas.models import *

class ProductoSerializer(serializers.ModelSerializer):
    # Permite seleccionar la marca desde la lista de marcas disponibles
    marca = serializers.PrimaryKeyRelatedField(queryset=MarcaProductos.objects.all())
    marca_descripcion = serializers.CharField(source='marca.descripcion', read_only=True)
    # Permite editar la imagen
    imagen = serializers.ImageField(required=False)

    class Meta:
        model = Producto
        fields = ['idProducto', 'nombre', 'descripcion', 'precio', 'stock', 'imagen', 'marca', 'categoria', 'marca_descripcion']

    def to_representation(self, instance):
        # Llama a la representación estándar del serializer
        representation = super().to_representation(instance)
        
        # Verifica si hay una imagen y agrega la URL completa
        if instance.imagen:
            # Retorna la URL completa de la imagen
            representation['imagen'] = instance.imagen.url  

        return representation

class MarcaProductosSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarcaProductos
        fields = '__all__'

class CategoriaProductosSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaProductos
        fields = '__all__'

