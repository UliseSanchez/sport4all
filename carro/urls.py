from django.urls import path
from . import views

app_name="carro"

urlpatterns = [
    path('agregar/<int:producto_id>/', views.agregar_producto, name="agregar"),
    path('restar/<int:producto_id>/', views.restar_producto, name="restar"),
    path('quitar/<int:producto_id>/', views.quitar_producto, name="quitar"),
    path('eliminar/', views.limpiar, name="eliminar")
]

