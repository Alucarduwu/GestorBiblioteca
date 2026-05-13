from django import forms
from django.db.models import Q
from .models import Prestamo, Libro, Usuario

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['usuario', 'libro', 'fecha_prestamo', 'fecha_devolucion', 'estado', 'observaciones']
        labels = {
            'usuario': 'Seleccionar Miembro',
            'libro': 'Libro a Prestar',
            'fecha_prestamo': 'Fecha de Inicio',
            'fecha_devolucion': 'Fecha de Devolución Estimada',
            'estado': 'Estado del Préstamo',
            'observaciones': 'Notas Internas',
        }
        widgets = {
            'fecha_prestamo': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control rounded-3'}),
            'fecha_devolucion': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control rounded-3'}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control rounded-3', 'placeholder': 'Detalles adicionales o estado del libro...'}),
            'usuario': forms.Select(attrs={'class': 'form-select rounded-3'}),
            'libro': forms.Select(attrs={'class': 'form-select rounded-3'}),
            'estado': forms.Select(attrs={'class': 'form-select rounded-3'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 1. Configuración de Selects (Eliminar guiones y mejorar labels)
        self.fields['usuario'].empty_label = "Elija un miembro..."
        self.fields['libro'].empty_label = "Elija un ejemplar disponible..."
        
        # 2. Filtrado de libros disponibles
        if not self.instance.pk:
            # En creación, solo libros disponibles
            self.fields['libro'].queryset = Libro.objects.filter(disponible=True)
        else:
            # En edición, permitir el libro actual + los disponibles
            self.fields['libro'].queryset = Libro.objects.filter(
                Q(disponible=True) | Q(pk=self.instance.libro.pk)
            )


        # 3. Validar si hay libros (para usar en el template)
        self.hay_libros = self.fields['libro'].queryset.exists()
        
        if not self.hay_libros:
            self.fields['libro'].widget.attrs['disabled'] = 'disabled'
            self.fields['libro'].help_text = "No hay ejemplares disponibles en este momento."

        # 4. Estilizar labels (opcional si se hace en template)
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = f"Ingrese {self.fields[field].label.lower()}"
