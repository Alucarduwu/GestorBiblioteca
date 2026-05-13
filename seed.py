import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from library.models import Autor, Usuario, Libro, Prestamo

def seed_data():
    print("Sembrando datos de ejemplo...")
    
    a1 = Autor.objects.create(
        nombre="Gabriel", 
        apellido="García Márquez", 
        nacionalidad="Colombiano", 
        fecha_nacimiento=date(1927, 3, 6)
    )
    a2 = Autor.objects.create(
        nombre="Miguel", 
        apellido="de Cervantes", 
        nacionalidad="Español", 
        fecha_nacimiento=date(1547, 9, 29)
    )
    
    u1 = Usuario.objects.create(
        nombre="Juan", 
        apellido="Pérez", 
        email="juan.perez@example.com", 
        telefono="555-0101"
    )
    u2 = Usuario.objects.create(
        nombre="María", 
        apellido="López", 
        email="maria.lopez@example.com", 
        telefono="555-0202"
    )
    
    l1 = Libro.objects.create(
        titulo="Cien años de soledad",
        isbn="9780307474728",
        descripcion="Una de las obras más importantes de la literatura hispana.",
        fecha_publicacion=date(1967, 5, 30),
        autor=a1
    )
    l2 = Libro.objects.create(
        titulo="Don Quijote de la Mancha",
        isbn="9788420412146",
        descripcion="La obra cumbre de la lengua española.",
        fecha_publicacion=date(1605, 1, 16),
        autor=a2
    )
    
    Prestamo.objects.create(
        usuario=u1,
        libro=l1,
        estado='ACTIVO',
        observaciones="Entregado en buen estado."
    )
    
    print("¡Datos sembrados con éxito!")

if __name__ == '__main__':
    seed_data()
