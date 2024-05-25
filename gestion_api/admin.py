from django.contrib import admin
from django.http.request import HttpRequest
from .models import *

class UsuarioAdmin(admin.ModelAdmin):
    list_display=("nombre", "rol", "estatus")
    serarch_fields=("rol", "estatus")
    list_filter=("estatus",)

class ProductoAdmin(admin.ModelAdmin):
    list_display=("nombre", "marca", "precio", "disponibilidad")
    serarch_fields=("nombre", "marca", "disponibilidad")
    def get_readonly_fields(self, request, obj=None):
        # Si el objeto ya está registrado, hace los campos readonly
        if obj and obj.id:
            return self.readonly_fields + ("nombre", "marca")
        # Si el objeto aún no está registrado, no hace cambios
        return self.readonly_fields
    def has_delete_permission(self, request, obj=None):
        return False

class ProveedorAdmin(admin.ModelAdmin):
    list_display=("nombre", "RFC", "estatus")
    serarch_fields=("nombre", "estatus")
    list_filter=("estatus",)
    def get_readonly_fields(self, request, obj=None):
        # Si el objeto ya está registrado, hace los campos readonly
        if obj and obj.id:
            return self.readonly_fields + ("nombre", "RFC")
        # Si el objeto aún no está registrado, no hace cambios
        return self.readonly_fields
    def has_delete_permission(self, request, obj=None):
        return False

class IvaAdmin(admin.ModelAdmin):
    list_display=("porcentaje","fecha","validez")
    search_fields=("fecha", "porcentaje")
    list_filter=("validez",)
    def get_readonly_fields(self, request, obj=None):
        # Si el objeto ya está registrado, hace los campos readonly
        if obj and obj.id:
            return self.readonly_fields + ("fecha", "porcentaje")
        # Si el objeto aún no está registrado, no hace cambios
        return self.readonly_fields
    def has_delete_permission(self, request, obj=None):
        return False
   
class VentaAdmin(admin.ModelAdmin):
    list_display=("fecha","estatus","IDCliente")
    search_fields=("fecha", "id")
    def get_readonly_fields(self, request, obj=None):
        # Si el objeto ya está registrado, hace los campos readonly
        if obj and obj.id:
            if obj.estatus=="Entregada" or obj.estatus=="Cancelada":
                return self.readonly_fields + ("fecha","IDCliente","estatus")    
            return self.readonly_fields + ("fecha","IDCliente")
        # Si el objeto aún no está registrado, no hace cambios
        return self.readonly_fields
    def has_add_permission(self, request):
        # Devuelve False para deshabilitar la capacidad de agregar nuevos objetos
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class VentaPAdmin(admin.ModelAdmin):
    list_display=("folio","cantidad_producto","IDProducto")
    def get_readonly_fields(self, request, obj=None):
        # Si el objeto ya está registrado, hace los campos readonly
        if obj and obj.id:
            return self.readonly_fields + ("folio","cantidad_producto","IDProducto")
        # Si el objeto aún no está registrado, no hace cambios
        return self.readonly_fields
    def has_add_permission(self, request):
        # Devuelve False para deshabilitar la capacidad de agregar nuevos objetos
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    
class CompraAdmin(admin.ModelAdmin):
    list_display=("fecha","estatus", "IDProveedor")
    search_fields=("fecha", "id")
    def get_readonly_fields(self, request, obj=None):
        # Si el objeto ya está registrado, hace los campos readonly
        if obj and obj.id:
            if obj.estatus=="Pagada" or obj.estatus=="Cancelada":
                return self.readonly_fields + ("fecha","IDProveedor","estatus")    
            return self.readonly_fields + ("fecha","IDProveedor")
        # Si el objeto aún no está registrado, no hace cambios
        return self.readonly_fields
    def has_add_permission(self, request):
        # Devuelve False para deshabilitar la capacidad de agregar nuevos objetos
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class CompraPAdmin(admin.ModelAdmin):
    list_display=("folio","cantidad_producto","IDProducto")
    def get_readonly_fields(self, request, obj=None):
        # Si el objeto ya está registrado, hace los campos readonly
        if obj and obj.id:
            return self.readonly_fields + ("folio","cantidad_producto","IDProducto")
        # Si el objeto aún no está registrado, no hace cambios
        return self.readonly_fields
    def has_add_permission(self, request):
        # Devuelve False para deshabilitar la capacidad de agregar nuevos objetos
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    
class AlmacenAdmin(admin.ModelAdmin):
    list_display=("IDproducto","stock_actual","stock_minimo","stock_maximo")
    def get_readonly_fields(self, request, obj=None):
        # Si el objeto ya está registrado, hace los campos readonly
        if obj and obj.id:
            return self.readonly_fields + ("IDproducto","stock_actual")
        # Si el objeto aún no está registrado, no hace cambios
        return self.readonly_fields
    def has_delete_permission(self, request, obj=None):
        return False
    
admin.site.register(Venta,VentaAdmin)  
admin.site.register(VentaProductos,VentaPAdmin)
admin.site.register(Compra,CompraAdmin)  
admin.site.register(Compra_Productos,CompraPAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Almacen,AlmacenAdmin)
admin.site.register(Iva, IvaAdmin)
