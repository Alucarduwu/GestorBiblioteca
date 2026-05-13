from django.urls import path
from .views import (
    PrestamoListView, PrestamoDetailView, PrestamoCreateView, 
    PrestamoUpdateView, PrestamoDeleteView
)

urlpatterns = [
    path('', PrestamoListView.as_view(), name='home'),
    path('prestamos/', PrestamoListView.as_view(), name='prestamo-list'),
    path('prestamos/nuevo/', PrestamoCreateView.as_view(), name='prestamo-create'),
    path('prestamos/<int:pk>/', PrestamoDetailView.as_view(), name='prestamo-detail'),
    path('prestamos/<int:pk>/editar/', PrestamoUpdateView.as_view(), name='prestamo-update'),
    path('prestamos/<int:pk>/eliminar/', PrestamoDeleteView.as_view(), name='prestamo-delete'),
]
