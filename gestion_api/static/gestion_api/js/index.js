
const listarProductos = async (idProveedor) => {
    try {
        const response = await fetch(`http://localhost:8000/sport4all/compra/obtener_productos/${idProveedor}`);
        const data = await response.json();
        if (data.message == "Success") {
            let opciones = '';
            data.productos.forEach((producto) => {
                opciones += `<option value='${producto.id}'>${producto.nombre}</option>`;
            });
            document.getElementById("productos").innerHTML = opciones;
        } else {
            alert("No hay productos registrados para ese proveedor");
            let opciones = '';
            document.getElementById("productos").innerHTML = opciones;
        }
    } catch (error) {
        console.log(error);
    }
};

const calcularTotal = async(idProducto)=>{
    try {
        const response = await fetch(`http://localhost:8000/sport4all/compra/obtener_producto/${idProducto}`);
        const data = await response.json();
        if (data.message == "Success") {
            let sub = '';
            let iva = '';
            let tot = '';
            let cantidad = parseInt(document.getElementById("cantidad").value,10)
            subtotal= parseInt(data.producto.precio,10);
            iva = (subtotal * data.iva)/100;
            total = subtotal + iva; 
            sub=`<td>${subtotal}</td>`;
            Iva=`<td>${iva}</td>`;
            tot=`<td>${total}</td>`;
            document.getElementById("subtotal").innerHTML = sub;
            document.getElementById("iva").innerHTML = Iva;
            document.getElementById("total").innerHTML = tot;
        } else {
            let sub = '';
            let iva = '';
            let tot = '';
            sub+=`<td>a</td>`;
            Iva+=` <td>a</td>`;
            tot+=` <td>a</td>`;
            document.getElementById("subtotal").innerHTML = sub;
            document.getElementById("iva").innerHTML = Iva;
            document.getElementById("total").innerHTML = tot;
        }
    
    } catch (error) {
        console.log(error);
    }
};

const cargaInicial = async () => {
    if (request.session.carro_compra.items){
        listarProveedores(request.session.carro_compra.items.producto_id)
        document.getElementById("proveedor").readOnly = true;
    }
    
    document.getElementById("proveedores").addEventListener("change", (event) => {
        listarProductos(event.target.value);
    });
    
};

window.addEventListener("load", async () => {
    await cargaInicial();
});

/*
$(document).ready(function () {
    $('#proveedor-selector').change(function () {
        var proveedorId = $(this).val();
        var productsUrl = $('#producto-selector').data('products-url');

        $.ajax({
            url: productsUrl,
            data: { '_id': proveedorId },
            success: function (data) {
                var productoSelector = $('#producto-selector');
                productoSelector.empty();
                productoSelector.append('<option value="">Selecciona un objeto</option>');
                $.each(data, function (key, value) {
                    productoSelector.append('<option value="' + value.id + '">' + value.nombre + '</option>');
                });
            }
        });
    });
});*/