from django.shortcuts import render, redirect
from  .carro import Carro
from  gestion_api.models import Producto, Venta, VentaProductos, Almacen
from django.contrib import messages

def agregar_producto(request, producto_id):
    carro=Carro(request)
    producto=Producto.objects.get(id=producto_id)
    stock=Almacen.objects.get(**{"IDproducto":producto.id})
    cantidad=int(carro.obtener_cantidad(producto))+stock.stock_actual
    if cantidad == stock.stock_maximo:
        messages.error(request, "No se pueden agregar más productos")
        return redirect("carrito") 
    carro.agregar_productos(producto=producto)
    return redirect("carrito")

def quitar_producto(request, producto_id):
    carro=Carro(request)
    producto=Producto.objects.get(id=producto_id)
    carro.eliminar_producto(producto=producto)
    return redirect("carrito")

def restar_producto(request, producto_id):
    carro=Carro(request)
    producto=Producto.objects.get(id=producto_id)
    carro.eliminar_unidad(producto=producto)
    return redirect("carrito")

def limpiar(request):
    carro=Carro(request)

    carro.limpiar_carro()
    return redirect("carrito")
