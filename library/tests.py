from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from rest_framework import status
from .models import Autor, Usuario, Libro, Prestamo
import datetime

class LibraryLogicTest(TestCase):
    def setUp(self):
        # Datos base para pruebas con campos obligatorios
        self.autor = Autor.objects.create(
            nombre="Gabriel", 
            apellido="García Márquez",
            nacionalidad="Colombiana",
            fecha_nacimiento=datetime.date(1927, 3, 6)
        )
        self.usuario = Usuario.objects.create(
            nombre="Juan", 
            apellido="Pérez", 
            email="juan@example.com",
            telefono="123456789"
        )
        self.libro = Libro.objects.create(
            titulo="Cien años de soledad", 
            autor=self.autor, 
            isbn="9780307474728",
            fecha_publicacion=datetime.date(1967, 5, 30)
        )
        self.api_client = APIClient()
        self.web_client = Client()

    # 1. Pruebas de Modelos
    def test_model_creation(self):
        """Verificando creacion correcta de modelos..."""
        self.assertEqual(Autor.objects.count(), 1)
        self.assertEqual(Usuario.objects.count(), 1)
        self.assertEqual(Libro.objects.count(), 1)
        self.assertTrue(self.libro.disponible)

    # 2. Pruebas de Logica de Prestamos
    def test_loan_availability_sync(self):
        """Validando sincronizacion de stock del libro..."""
        prestamo = Prestamo.objects.create(
            usuario=self.usuario,
            libro=self.libro,
            estado='ACTIVO'
        )
        self.libro.refresh_from_db()
        self.assertFalse(self.libro.disponible)

        prestamo.estado = 'DEVUELTO'
        prestamo.save()
        self.libro.refresh_from_db()
        self.assertTrue(self.libro.disponible)

    def test_prevent_duplicate_active_loans(self):
        """Bloqueando prestamos duplicados activos..."""
        Prestamo.objects.create(usuario=self.usuario, libro=self.libro, estado='ACTIVO')
        segundo_prestamo = Prestamo(usuario=self.usuario, libro=self.libro, estado='ACTIVO')
        with self.assertRaises(ValidationError):
            segundo_prestamo.clean()

    def test_prevent_loan_unavailable_book(self):
        """Previniendo prestamo de libros sin stock..."""
        self.libro.disponible = False
        self.libro.save()
        prestamo = Prestamo(usuario=self.usuario, libro=self.libro, estado='ACTIVO')
        with self.assertRaises(ValidationError):
            prestamo.clean()

    # 3. Pruebas de API REST
    def test_api_endpoints(self):
        """Comprobando estabilidad de endpoints API..."""
        endpoints = ['/api/autores/', '/api/usuarios/', '/api/libros/', '/api/prestamos/']
        for url in endpoints:
            response = self.api_client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    # 4. Pruebas de CRUD Web
    def test_web_views(self):
        """Verificando accesibilidad de vistas web..."""
        response = self.web_client.get(reverse('prestamo-list'))
        self.assertEqual(response.status_code, 200)
        response = self.web_client.get(reverse('prestamo-create'))
        self.assertEqual(response.status_code, 200)
