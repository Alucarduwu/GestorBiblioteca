from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AutorViewSet, UsuarioViewSet, LibroViewSet, PrestamoViewSet,
    DashboardView, APIDocumentationView,
    PrestamoListView, PrestamoDetailView, PrestamoCreateView, 
    PrestamoUpdateView, PrestamoDeleteView
)


router = DefaultRouter()
router.register(r'autores', AutorViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'libros', LibroViewSet)
router.register(r'prestamos', PrestamoViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    
    path('', DashboardView.as_view(), name='home'),
    path('api-docs/', APIDocumentationView.as_view(), name='api-docs-page'),
    path('prestamos/', PrestamoListView.as_view(), name='prestamo-list'),
    path('prestamos/nuevo/', PrestamoCreateView.as_view(), name='prestamo-create'),
    path('prestamos/<int:pk>/', PrestamoDetailView.as_view(), name='prestamo-detail'),
    path('prestamos/<int:pk>/editar/', PrestamoUpdateView.as_view(), name='prestamo-update'),
    path('prestamos/<int:pk>/eliminar/', PrestamoDeleteView.as_view(), name='prestamo-delete'),
]

