from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Count, Q
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Autor, Usuario, Libro, Prestamo
from .serializers import AutorSerializer, UsuarioSerializer, LibroSerializer, PrestamoSerializer
from .forms import PrestamoForm


class DashboardView(TemplateView):
    template_name = 'library/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_prestamos'] = Prestamo.objects.count()
        context['prestamos_activos'] = Prestamo.objects.filter(estado='ACTIVO').count()
        context['prestamos_devueltos'] = Prestamo.objects.filter(estado='DEVUELTO').count()
        context['libros_disponibles'] = Libro.objects.filter(disponible=True).count()
        context['recientes'] = Prestamo.objects.select_related('libro', 'usuario').order_by('-created_at')[:5]
        return context

class APIDocumentationView(TemplateView):
    template_name = 'library/api_docs.html'



class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nacionalidad']
    search_fields = ['nombre', 'apellido']
    ordering_fields = ['apellido', 'created_at']


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['activo']
    search_fields = ['nombre', 'apellido', 'email']
    ordering_fields = ['created_at']


class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['disponible', 'autor']
    search_fields = ['titulo', 'isbn']
    ordering_fields = ['fecha_publicacion', 'created_at']


class PrestamoViewSet(viewsets.ModelViewSet):
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['estado', 'usuario', 'libro']
    search_fields = ['observaciones']
    ordering_fields = ['fecha_prestamo', 'created_at']



class PrestamoListView(ListView):
    model = Prestamo
    template_name = 'library/prestamo_list.html'
    context_object_name = 'prestamos'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset



class PrestamoDetailView(DetailView):
    model = Prestamo
    template_name = 'library/prestamo_detail.html'
    context_object_name = 'prestamo'


class PrestamoCreateView(CreateView):
    model = Prestamo
    form_class = PrestamoForm
    template_name = 'library/prestamo_form.html'
    success_url = reverse_lazy('prestamo-list')

    def form_valid(self, form):
        messages.success(self.request, "Préstamo registrado exitosamente.")
        return super().form_valid(form)


class PrestamoUpdateView(UpdateView):
    model = Prestamo
    form_class = PrestamoForm
    template_name = 'library/prestamo_form.html'
    success_url = reverse_lazy('prestamo-list')

    def form_valid(self, form):
        messages.success(self.request, "Préstamo actualizado exitosamente.")
        return super().form_valid(form)


class PrestamoDeleteView(DeleteView):
    model = Prestamo
    template_name = 'library/prestamo_confirm_delete.html'
    success_url = reverse_lazy('prestamo-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Préstamo eliminado correctamente.")
        return super().delete(request, *args, **kwargs)
