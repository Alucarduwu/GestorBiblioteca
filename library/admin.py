from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Autor, Usuario, Libro, Prestamo

# --- Resources for Import/Export ---

class AutorResource(resources.ModelResource):
    class Meta:
        model = Autor

class UsuarioResource(resources.ModelResource):
    class Meta:
        model = Usuario

class LibroResource(resources.ModelResource):
    class Meta:
        model = Libro

class PrestamoResource(resources.ModelResource):
    class Meta:
        model = Prestamo

# --- Admin Registrations ---

@admin.register(Autor)
class AutorAdmin(ImportExportModelAdmin):
    resource_class = AutorResource
    list_display = ('nombre', 'apellido', 'nacionalidad', 'fecha_nacimiento', 'created_at')
    search_fields = ('nombre', 'apellido', 'nacionalidad')
    list_filter = ('nacionalidad',)
    ordering = ('apellido',)

@admin.register(Usuario)
class UsuarioAdmin(ImportExportModelAdmin):
    resource_class = UsuarioResource
    list_display = ('nombre', 'apellido', 'email', 'telefono', 'activo', 'created_at')
    search_fields = ('nombre', 'apellido', 'email')
    list_filter = ('activo',)
    ordering = ('-created_at',)

@admin.register(Libro)
class LibroAdmin(ImportExportModelAdmin):
    resource_class = LibroResource
    list_display = ('titulo', 'isbn', 'autor', 'disponible', 'fecha_publicacion')
    search_fields = ('titulo', 'isbn', 'autor__nombre', 'autor__apellido')
    list_filter = ('disponible', 'autor')
    ordering = ('titulo',)

@admin.register(Prestamo)
class PrestamoAdmin(ImportExportModelAdmin):
    resource_class = PrestamoResource
    list_display = ('libro', 'usuario', 'fecha_prestamo', 'fecha_devolucion', 'estado')
    search_fields = ('libro__titulo', 'usuario__nombre', 'usuario__apellido', 'estado')
    list_filter = ('estado', 'fecha_prestamo')
    ordering = ('-fecha_prestamo',)
