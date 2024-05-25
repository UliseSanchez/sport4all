from gestion_api.models import Iva
from django.utils import timezone

def importe_total_carro(request):
    total=0
    subtotal=0
    fecha = timezone.now().date()
    carro = request.session.get("carro", {})
    if request.user.is_authenticated:
        for key,value in carro.items():
            subtotal=subtotal+float(value["precio"])
        iva=(subtotal*Iva.objects.get(validez=True).porcentaje)/100
        total=subtotal+iva
        return{"importe_total_carro":total,"subtotal":subtotal,"IVA":iva, 'fecha':fecha}     
            