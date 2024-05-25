class carroCompra:
    def __init__(self, request):
        self.request=request
        self.session = request.session
        carro_compra=self.session.get("carro_compra")
        if not carro_compra:
            carro_compra=self.session["carro_compra"]={}
        self.carro_compra=carro_compra
    
    def agregar_productos(self,producto, cantidad):
        if(str(producto.id) not in self.carro_compra.keys()):
            self.carro_compra[producto.id]={
                "producto_id":producto.id,
                "nombre": producto.nombre,
                "marca": str(producto.marca),
                "precio": str(producto.precio*cantidad),
                "cantidad":cantidad
            }
        else:
            for key, value in self.carro_compra.items():
                if key==str(producto.id):
                    value["cantidad"]=value["cantidad"]+cantidad
                    value["precio"]=float(value["precio"])+producto.precio
                    break
        self.guardar_carro()
        
    def guardar_carro(self):
        self.session["carro_compra"]=self.carro_compra
        self.session.modified=True
    
    def eliminar_producto(self,producto):
        producto.id=str(producto.id)
        if producto.id in self.carro_compra:
            del self.carro_compra[producto.id]
            self.guardar_carro()
    
    def eliminar_unidad(self,producto):
        for key, value in self.carro_compra.items():
            if key==str(producto.id):
                value["cantidad"]=value["cantidad"]-1
                value["precio"]=float(value["precio"])-producto.precio
                if value["cantidad"]<1:
                    self.eliminar_producto(producto)
                break
        self.guardar_carro()
    
    def limpiar_carro(self):
        self.session["carro_compra"]={}
        self.session.modified=True
    
    def obtener_cantidad(self,producto):
        if(str(producto.id) not in self.carro_compra.keys()):
            return 0
        else:
            for key, value in self.carro_compra.items():
                if key==str(producto.id):
                    cantidad=value["cantidad"]
                    return cantidad
