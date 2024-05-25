from gestion_api.models import Iva

def importe_total_carro(request):
    total=0
    subtotal=0
    carro = request.session.get("carro_compra", {})
    if request.user.is_authenticated:
        for key,value in carro.items():
            subtotal=subtotal+float(value["precio"])
        iva=(subtotal*Iva.objects.get(validez=True).porcentaje)/100
        total=subtotal+iva
        return{"importe_total":total,"subtotal_carro":subtotal,"IVA_carro":iva}      

def contador_stock(request):
    stockAumentado=0
    carro = request.session.get("carro_compra", {})
    if request.user.is_authenticated:
        for key,value in carro.items():
            stockAumentado=stockAumentado+int(value["cantidad"])
        
        return{"contador_stock":stockAumentado}           