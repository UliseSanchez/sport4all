from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models import F,Sum, FloatField
#from django.utils import timezone

class Proveedor(models.Model):
    nombre=models.CharField(max_length=30)
    RFC=models.CharField(max_length=12)
    estatus = models.BooleanField(default=True)
    def __str__(self) -> str:
        return str(self.nombre)
    class Meta:
        verbose_name='proveedor'
        verbose_name_plural='proveedores'
        db_table='proveedores'

class Usuario(models.Model):
    ROLES = [("admin", "Administrador"), ("empleado", "Empleado"), ("cliente", "Cliente")]
    nombre = models.CharField(max_length=50)
    nombre_usuario = models.CharField(max_length=18)
    rol= models.CharField(max_length=20, choices=ROLES, default="Administrador")
    correo = models.EmailField()
    contrasenia = models.CharField(max_length=18)
    estatus = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.nombre)
    
 
class Talla_Producto(models.Model):
    TALLAS = [('CH', 'CH'), ('M', 'M'), ('L', 'L')]
    talla = models.CharField(max_length=2, choices=TALLAS, primary_key=True)
    def __str__(self):
        return str(self.talla)
    class Meta:
        db_table="tallas"
 
class Producto(models.Model):
    nombre = models.CharField(max_length=40)
    marca = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    descripcion = models.TextField(default="Sin descripcion")
    talla = models.ForeignKey(Talla_Producto, on_delete=models.CASCADE)
    precio = models.FloatField()
    imagen =models.ImageField(null=True, upload_to='producto')
    disponibilidad = models.BooleanField(default=True)
    #Agregar created y updated
    def __str__(self):
        return str(self.nombre)
    class Meta:
        db_table='productos'
        verbose_name='producto'
        verbose_name_plural='productos'

class Almacen(models.Model):  
    IDproducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    stock_minimo = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(limit_value=1)])
    stock_maximo = models.PositiveSmallIntegerField(default=255, validators=[MinValueValidator(limit_value=1)])
    stock_actual = models.PositiveSmallIntegerField(default = 1,  validators=[MinValueValidator(limit_value=1), 
                                                                 MaxValueValidator(limit_value=255)])
    def clean(self):
        if self.stock_maximo <= self.stock_minimo:
            raise ValidationError('El stock maximo debe ser mayor al stock minimo')
        if self.stock_actual < self.stock_minimo:
            raise ValidationError('El stock actual debe ser mayor al stock minimo')
        if self.stock_actual > self.stock_maximo:
            raise ValidationError('El stock actual debe ser menor al stock maximo')
        if Almacen.objects.filter(IDproducto=self.IDproducto):
            raise ValidationError('Este producto ya está registrado en el almacen')
    class Meta:
        db_table='stock'
        verbose_name='almacen'
        verbose_name_plural='almacen'

class Venta(models.Model):
    OPCIONES_ESTATUS = [("Procesando", "Procesando"), ("Cancelada", "Cancelada"),
                        ("En camino", "En transito"), ('Entregada', 'Entregada') ]
    fecha = models.DateField(auto_now_add=True)
    IDCliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estatus = models.CharField(max_length=20, choices=OPCIONES_ESTATUS, default='Procesando')
    class Meta:
        db_table='ventas'
        verbose_name='venta'
        verbose_name_plural='ventas'
   

"""@property
    def total(self):
        return self.ventaproductos_set.aggregate(
            total=Sum(F("precio")*F("cantidad_producto"), output_field=FloatField())
        )["total"] or FloatField(0)"""

class VentaProductos(models.Model):
    folio = models.ForeignKey(Venta, on_delete=models.CASCADE)
    IDProducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_producto = models.IntegerField()
    class Meta:
        db_table='ventas_productos'
        verbose_name='venta_producto'
        verbose_name_plural='ventas_productos'
    
           
class Compra(models.Model):
    IDProveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    OPCIONES_ESTATUS = [("Cancelada", "Cancelada"), ("Entregada", "Entregada"), ("Pagada", "Pagada")]
    fecha = models.DateField(auto_now_add=True) 
    #IDEmpleado = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estatus = models.CharField(max_length=20, choices=OPCIONES_ESTATUS, default='entregada')
    
    @property
    def total(self):
        return self.compra_productos_set.aggregate(
            total=Sum(F("precio")*F("cantidad_producto"), output_field=FloatField())
        )["total"]
    
    class Meta:
        verbose_name='compra'
        verbose_name_plural='compras'

class Compra_Productos(models.Model):
    folio = models.ForeignKey(Compra, on_delete=models.CASCADE)
    IDProducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_producto = models.IntegerField()
    def __str__(self):
        return f'{self.cantidad_producto} unidades de {self.IDProducto.nombre}'
    class Meta:
        db_table='compras_productos'
        verbose_name='compra_producto'
        verbose_name_plural='compras_productos'
    
class Iva(models.Model):
    fecha = models.DateField()
    porcentaje = models.IntegerField()
    validez = models.BooleanField(default=False)
    def clean(self):
        # Verificar si el valor de validez ya existe en otro objeto Iva
        if Iva.objects.filter(validez=True).exclude(pk=self.pk).exists():
            raise ValidationError('Ya existe un IVA valido, por favor desmarque la casilla de "Validez"')
    class Meta:
        db_table='IVA'
        verbose_name='IVA'
        verbose_name_plural='IVAs'


        
    
