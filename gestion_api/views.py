from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,  get_object_or_404, redirect
from carro.carro import Carro
from gestion_api.compra import carroCompra
from gestion_api.context_processor import contador_stock
from gestion_api.models import Producto, Compra, Almacen, Proveedor, Compra_Productos, Iva, Usuario, Venta, VentaProductos
from gestion_api.forms import FormularioCompra,BusquedaCompra, ModificarCompra
from django.contrib import messages

class AuxCompra:
    def __init__(self, folio, IDProducto, cantidad_producto):
        self.folio=folio
        self.IDProducto = IDProducto
        self.cantidad_producto=cantidad_producto
        

def home(request):
    return render(request, "index.html",{})

def consulta(request,pk):
    compra=get_object_or_404(Compra,pk=pk)
    if request.method=='POST':
        form=ModificarCompra(request.POST, instance=compra)
        if form.is_valid():
            id_compra_productos=Compra_Productos.objects.get(folio=pk)
            id_producto=id_compra_productos.IDProducto
            stock=Almacen.objects.get(**{'IDproducto': id_producto})
            estatus = form.cleaned_data['estatus']
            compra.estatus = estatus
            compra.save()
        #Aumentar stock si esta pagado
            if estatus=="Pagada":
                stock.stock_actual+=id_compra_productos.cantidad_producto
                stock.save()
                messages.success(request, 'Se actualizo correctamente la compra')
                return redirect("buscar")
            #else no hace nada
    else:
        form=ModificarCompra()
    return render(request, "resultado_busqueda.html", {'form': form, 'pk': compra.pk, 'compra':compra})

def buscar(request):
    if request.method =='POST':
        form=BusquedaCompra(request.POST)
        if form.is_valid():
            id = form.cleaned_data['buscar']
            try:
                compra=Compra.objects.get(pk=id)
                if(compra.estatus != "Pagada"):
                    return redirect('consulta', pk=id)
                else:
                    messages.error(request, 'No se puede modificar la compra si ya está pagada')
            except:
                messages.error(request, 'No se pudo encontrar la compra')
    else:
        form = BusquedaCompra()
    compras = Compra.objects.all()
    totales = {}
    ivas={}
    ivas = Iva.objects.all()
    compras_dict={} 
    for compra in compras:
        if compra.estatus != "cancelada":
            compras_list=[]
            proveedores={}
            subtotal_compra=0
            total_compra=0
            iva_compra=0
            totales={}
            fecha = compra.fecha
            for i in ivas:
                if fecha > i.fecha:
                    porcentaje_iva=i.porcentaje
            compra_producto= Compra_Productos.objects.filter(folio=compra.id)
            for comprap in compra_producto:       
                compras_list.append(comprap)
                prod=Producto.objects.get(pk=comprap.IDProducto_id)
                subtotal=int(prod.precio)*int(comprap.cantidad_producto)
                iva=(subtotal*porcentaje_iva)/100
                proveedores[comprap.id]=prod.marca
                totales[comprap.id]=subtotal
                subtotal_compra=subtotal_compra+subtotal
                iva_compra=iva_compra+iva
                
            total_compra=subtotal_compra+iva_compra
            compras_dict[compra.id]={
                "compra_productos":compras_list,
                "fecha":fecha,
                "estatus": compra.estatus,
                "proveedores":proveedores,
                "subtotal":subtotal_compra,
                "iva":iva_compra,
                "total":total_compra,
                "totales":totales
            }

    return render(request, 'formulario.html', {'form': form, 'compras':compras_dict})

def agregar_producto(request, producto_id, cantidad):
    producto=Producto.objects.get(id=producto_id)
    carro=carroCompra(request)
    stock=Almacen.objects.get(**{'IDproducto': producto.id})
    cont = carro.obtener_cantidad(producto)
    stock_actual= int(cont)+stock.stock_actual
    if stock_actual > stock.stock_maximo:
        messages.error(request, 'No se puede agregar mas cantidad que la del stock maximo')
        return redirect("compra") 
    carro.agregar_productos(producto=producto, cantidad=cantidad)
    
    return redirect("compra")

def quitar_producto(request, producto_id):
    carro=carroCompra(request)
    producto=Producto.objects.get(id=producto_id)
    carro.eliminar_producto(producto=producto)
    return redirect("compra")

def restar_producto(request, producto_id):
    carro=carroCompra(request)
    producto=Producto.objects.get(id=producto_id)
    carro.eliminar_unidad(producto=producto)
    return redirect("compra")

def limpiar(request):
    carro=carroCompra(request)

    carro.limpiar_carro()
    return redirect("compra")

def registrar_compra(request):
    carro=carroCompra(request)
    fecha = timezone.now().date()
    if request.method == "POST":
        form = FormularioCompra(request.POST)
        if form.is_valid():
            dataform = form.cleaned_data
            qs= Compra.objects.values_list('id', flat=True).last()
            folio = qs + 1
            #Obtener Id del producto
            prod = Producto.objects.get(nombre=dataform['producto'])
            id_producto=prod.id
            cantidad = int(dataform['cantidad'])
            stock=Almacen.objects.get(**{'IDproducto': id_producto})
            carro=carroCompra(request) 
            cont = carro.obtener_cantidad(producto=prod)
            stock_actual= int(cont)+stock.stock_actual+cantidad
            
            if stock_actual > stock.stock_maximo:
                messages.error(request, 'No se puede agregar mas cantidad que la del stock maximo')  
            else:
                agregar_producto(request,producto_id=id_producto, cantidad=cantidad)
    else:
        form=FormularioCompra()
    return render(request, "compra.html",{"form":form, "fecha":fecha})

def concluir_compra(request):
    carro=carroCompra(request)    
    productos_compra=list()
    cont=0
    if not carro.carro_compra.items():
        messages.error(request, "El pedido no se ha generado correctamente")
        return redirect("compra")
    for key,value in carro.carro_compra.items():
        producto=Producto.objects.get(pk=key)
        if cont==0:
            proveedor=Proveedor.objects.get(**{"nombre":value["marca"]})    
            compra=Compra.objects.create(IDProveedor=proveedor)
            cont=1
        productos_compra.append(Compra_Productos(
            folio = compra,
            IDProducto = producto,
            cantidad_producto = value["cantidad"]   
        ))
    Compra_Productos.objects.bulk_create(productos_compra)
    messages.success(request, "El pedido se ha generado correctamente")
    carro.limpiar_carro()
    return redirect("buscar")

def venta(request):
    productos=Producto.objects.all()
    return render(request, "venta.html",{"productos":productos})

def carrito(request):
    qs= Venta.objects.values_list('id', flat=True).last()
    folio = qs + 1
    usuario = request.user.username
    return render(request, "carrito.html",{"folio":folio, "usuario":usuario})

def historial(request):
    usuario = request.user.username
    cliente = Usuario.objects.get(**{"nombre_usuario":usuario})
    ventas = Venta.objects.all()
    ivas = Iva.objects.all()
    ventas_dict={} 
    for venta in ventas:
        if (venta.estatus != "Cancelada") & (venta.IDCliente == cliente) :
            ventas_list=[]
            subtotal_venta=0
            total_venta=0
            iva_venta=0
            totales={}
            marcas={}
            fecha = venta.fecha
            for i in ivas:
                if fecha > i.fecha:
                    porcentaje_iva=i.porcentaje
            venta_producto= VentaProductos.objects.filter(folio=venta.id)
            for ventap in venta_producto:       
                ventas_list.append(ventap)
                prod=Producto.objects.get(pk=ventap.IDProducto_id)
                subtotal=int(prod.precio)*int(ventap.cantidad_producto)
                iva=(subtotal*porcentaje_iva)/100
                marcas[ventap.id]=prod.marca
                totales[ventap.id]=subtotal
                subtotal_venta=subtotal_venta+subtotal
                iva_venta=iva_venta+iva
                
            total_venta=subtotal_venta+iva_venta
            ventas_dict[venta.id]={
                "ventas_productos":ventas_list,
                "fecha":fecha,
                "estatus": venta.estatus,
                "marcas":marcas,
                "subtotal":subtotal_venta,
                "iva":iva_venta,
                "total":total_venta,
                "totales":totales
            }
    return render(request, "historial.html", {"ventas":ventas_dict, "usuario":usuario})

def pagar(request):
    usuario=Usuario.objects.get(pk=1)
    pedido=Venta.objects.create(IDCliente=usuario)
    carro=Carro(request)
    productos_venta=list()
    for key,value in carro.carro.items():
        producto=Producto.objects.get(pk=key)
        productos_venta.append(VentaProductos(
            folio = pedido,
            IDProducto = producto,
            cantidad_producto = value["cantidad"]   
        ))
    VentaProductos.objects.bulk_create(productos_venta)
    messages.success(request, "El pedido se ha generado correctamente")
    carro.limpiar_carro()
    return redirect("carrito")

def prueba(request):
    return render(request, "base3.html")

def obtener_proveedores(request, id):
    proveedores = list(Proveedor.objects.get(pk=id))
    if (len(proveedores)>0):
        data={'message':"Success", 'proveedores':proveedores}
    else:
        data={'message':"Not Found"}
    return JsonResponse(data)

def obtener_productos(request, proveedor):
    productos= list(Producto.objects.filter(marca=proveedor).values())
    if (len(productos)>0):
        data={'message':"Success", 'productos':productos}
    else:
        data={'message':"Not Found"}
    return JsonResponse(data)


def obtener_producto(request, id_producto):
    producto= list(Producto.objects.filter(pk=id_producto).values())
    iva= list(Iva.objects.filter(validez=True).values())
    if (len(producto)>0):
        data={'message':"Success", 'producto':producto, 'iva':iva}
    else:
        data={'message':"Not Found"}
    return JsonResponse(data)

