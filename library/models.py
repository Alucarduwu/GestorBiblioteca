from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Autores"
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.email})"


class Libro(models.Model):
    titulo = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    descripcion = models.TextField(blank=True)
    fecha_publicacion = models.DateField()
    disponible = models.BooleanField(default=True)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class Prestamo(models.Model):
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('DEVUELTO', 'Devuelto'),
        ('ATRASADO', 'Atrasado'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='prestamos')
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='prestamos')
    fecha_prestamo = models.DateField(default=timezone.now)
    fecha_devolucion = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='ACTIVO')
    observaciones = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.pk:
            if not self.libro.disponible:
                raise ValidationError(f"El libro '{self.libro.titulo}' no está disponible para préstamo.")
            
            if Prestamo.objects.filter(libro=self.libro, estado='ACTIVO').exists():
                raise ValidationError(f"El libro '{self.libro.titulo}' ya tiene un préstamo activo.")

    def save(self, *args, **kwargs):
        self.full_clean()
        
        is_new = self.pk is None
        old_status = None
        
        if not is_new:
            old_status = Prestamo.objects.get(pk=self.pk).estado

        super().save(*args, **kwargs)

        if is_new and self.estado == 'ACTIVO':
            self.libro.disponible = False
            self.libro.save()
        elif old_status == 'ACTIVO' and self.estado == 'DEVUELTO':
            self.libro.disponible = True
            self.libro.save()

    def __str__(self):
        return f"Préstamo: {self.libro.titulo} - {self.usuario.nombre}"
