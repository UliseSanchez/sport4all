from django.urls import path
from gestion_api import views

urlpatterns = [
    path('', views.home, name="home"),
    path('consulta/<int:pk>/', views.consulta, name="consulta"),
    path("buscar/", views.buscar, name="buscar"),
    path("compra/",views.registrar_compra, name="compra"),
    path("productos/", views.venta, name="venta"),
    path("carrito/", views.carrito, name="carrito"),
    path('compra/obtener_producto/<int:id_producto>', views.obtener_producto, name='obtener_productos_por_proveedor'),
    path('compra/obtener_proveedor/<int:id>', views.obtener_proveedores, name='obtener_proveedores'),
    path('compra/obtener_productos/<int:proveedor>', views.obtener_productos, name='obtener_productos'),
    path("prueba/",views.prueba,name="prueba"),
    path("pagar/",views.pagar,name="pagar"),
    path("mi_cuenta/",views.historial,name="mi_cuenta"),
    path('compra/concluir_compra/',views.concluir_compra, name="concluir_compra")
]

