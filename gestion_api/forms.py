from django import forms
from django.urls import reverse_lazy
from gestion_api.models import Producto, Compra, Proveedor, Compra_Productos,Almacen


class FormularioCompra(forms.Form):
    class Meta:
        model = Compra
        fields = '__all__'
    
            
    OPCIONES_ESTATUS = [("procesando", "En proceso"), ("cancelada", "Cancelada"), 
                        ("entregada", "Entregada"), ("pagada", "Pagada")]
    qs= Compra.objects.values_list('id', flat=True).last()
    folio = qs + 1
    proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.filter(estatus=True), empty_label="Selecciona un proveedor",
                                       widget=forms.Select(attrs={'id': 'proveedores'}))
    producto = forms.ModelChoiceField(queryset=Producto.objects.filter(disponibilidad=True), empty_label="Selecciona un producto", 
                                      widget=forms.Select(attrs={'id':'productos'}))
    cantidad = forms.IntegerField(max_value=255, min_value=1)   
    """fecha = forms.DateField(
        widget=forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
            }
        )
    )"""


    
    
class PartiallyReadOnlyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PartiallyReadOnlyForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Desactivar todos los campos excepto el que deseas permitir la edición
            if field_name != 'campo_permisible':
                field.widget.attrs['readonly'] = True
                field.widget.attrs['disabled'] = True  
 
class ModificarCompra(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['estatus']
    

class BusquedaCompra(forms.Form):
    buscar=forms.IntegerField(label='Folio')