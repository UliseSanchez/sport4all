from django.urls import path
from gestion_api import views

app_name="carro_compra"

urlpatterns = [
    path('agregar/<int:producto_id>/<int:cantidad>/', views.agregar_producto, name="agregar"),
    path('restar/<int:producto_id>/', views.restar_producto, name="restar"),
    path('quitar/<int:producto_id>/', views.quitar_producto, name="quitar"),
    path('vaciar/', views.limpiar, name="vaciar")
]