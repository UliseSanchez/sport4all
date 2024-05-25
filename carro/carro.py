class Carro:
    def __init__(self, request):
        self.request=request
        self.session = request.session
        carro=self.session.get("carro")
        if not carro:
            carro=self.session["carro"]={}
        self.carro=carro
    
    def agregar_productos(self,producto):
        if(str(producto.id) not in self.carro.keys()):
            self.carro[producto.id]={
                "producto_id":producto.id,
                "nombre": producto.nombre,
                "marca": str(producto.marca),
                "talla": str(producto.talla),
                "precio": str(producto.precio),
                "cantidad":1,
                "imagen":producto.imagen.url
            }
        else:
            for key, value in self.carro.items():
                if key==str(producto.id):
                    value["cantidad"]=value["cantidad"]+1
                    value["precio"]=float(value["precio"])+producto.precio
                    break
        self.guardar_carro()
        
    def guardar_carro(self):
        self.session["carro"]=self.carro
        self.session.modified=True
    
    def eliminar_producto(self,producto):
        producto.id=str(producto.id)
        if producto.id in self.carro:
            del self.carro[producto.id]
            self.guardar_carro()
    
    def eliminar_unidad(self,producto):
        for key, value in self.carro.items():
            if key==str(producto.id):
                value["cantidad"]=value["cantidad"]-1
                value["precio"]=float(value["precio"])-producto.precio
                if value["cantidad"]<1:
                    self.eliminar_producto(producto)
                break
        self.guardar_carro()
    
    def limpiar_carro(self):
        self.session["carro"]={}
        self.session.modified=True
        
    def obtener_cantidad(self,producto):
        if(str(producto.id) not in self.carro.keys()):
            return 0
        else:
            for key, value in self.carro.items():
                if key==str(producto.id):
                    cantidad=value["cantidad"]+1
                    return cantidad