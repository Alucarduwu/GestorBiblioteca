from rest_framework import serializers
from .models import Autor, Usuario, Libro, Prestamo

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'


class LibroSerializer(serializers.ModelSerializer):
    autor_nombre = serializers.CharField(source='autor.__str__', read_only=True)

    class Meta:
        model = Libro
        fields = '__all__'


class PrestamoSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.__str__', read_only=True)
    libro_titulo = serializers.CharField(source='libro.titulo', read_only=True)

    class Meta:
        model = Prestamo
        fields = '__all__'
    
    def validate(self, data):
        # Additional validation can go here if needed, 
        # though model clean() handles core business rules.
        return data
