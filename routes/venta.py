from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify, session
from controllers.stock import obtener_categorias,obtener_productos_de_categoria,verificar_stock, calcular_valor_total, descontar_stock_pedido,buscar_precio
from controllers.venta import cargar_venta,cargar_detalle_venta
from utils.decoradores import login_required, role_required


venta_bp = Blueprint('venta', __name__)

############## Ruta de ventana original
@venta_bp.route('/venta')
@login_required
@role_required('administrador', 'vendedor', 'cajero')
def venta():
    """ Ruta que lleva a la ventana venta con los productos """
    categorias = obtener_categorias()
    return render_template('venta.html', categorias=categorias)

############## Ruta Buscar una categoria
@venta_bp.route('/venta/buscar-categoria/<int:id_categoria>')
@login_required
@role_required('administrador', 'vendedor', 'cajero')
def buscar_categoria_route(id_categoria):
    """ Busco una categoria para mostrar los elementos """
    productos = obtener_productos_de_categoria(id_categoria)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Petición AJAX → solo fragmento HTML
        return render_template('ventaLista.html', productos=productos)

    # Petición normal → vista completa
    categorias = obtener_categorias()
    return render_template('ventaLista.html', productos=productos, categorias=categorias)

############## Ruta agregar una venta
# @venta_bp.route('/venta/crear-venta', methods=['POST'])
# @login_required
# @role_required('administrador', 'vendedor', 'cajero')
# def cargar_venta_route():
#     """ Ruta que carga un pedido a la base """
    
#     pedido = request.get_json()
    
#     # 1ro Verifico que el pedido no esté vacío y que haya stock
#     stock_ok = verificar_stock(pedido)
    
#     #si el pedido esta ok, cargo la venta y descuento el stock usando una función del controlador
#     if stock_ok["estado"]:
#         # descuento el stock de los productos
#         resultado2 = descontar_stock_pedido(pedido)
        
#         if resultado2:
#             # Obtengo el usuario de la sesión
#             dni_usuario = session.get("usuario")

#             # busco los productos del pedido, sumo el valor de cada uno , lo guardo en valor_total y lo guardo en la base
#             valor_total = calcular_valor_total(pedido)
#             # cargo la venta y el detalle
#             resultado = cargar_venta(dni_usuario, valor_total)
            
            
#             if resultado:
#                 mensajes(resultado, "✅ Venta cargada correctamente.")
#                 return jsonify({"success": True, "message": "Venta cargada correctamente."})
#             else:
#                 mensajes(resultado, "❌ Error al cargar la venta.")
#                 return jsonify({"success": False, "message": "Error al cargar la venta."})
        
#     return jsonify({"success": stock_ok["estado"], "message": stock_ok["error"]})

@venta_bp.route('/venta/crear-venta', methods=['POST'])
@login_required
@role_required('administrador', 'vendedor', 'cajero')
def cargar_venta_route():
    """ Ruta que carga un pedido a la base """

    pedido = request.get_json()

    # 1. Verificar stock de todos los productos
    stock_ok = verificar_stock(pedido)
    if not stock_ok["estado"]:
        return jsonify({"success": False, "message": stock_ok["error"]})

    # 2. Calcular valor total de la venta
    valor_total = calcular_valor_total(pedido)

    # 3. Obtener DNI del usuario desde sesión
    dni_usuario = session.get("usuario")
    if not dni_usuario:
        return jsonify({"success": False, "message": "Usuario no autenticado"})

    # 4. Registrar venta y obtener ID
    id_venta = cargar_venta(dni_usuario, valor_total)
    if not id_venta:
        return jsonify({"success": False, "message": "Error al cargar la venta"})

    # 5. Registrar detalles de la venta
    for item in pedido:
        id_producto = item.get("id")
        cantidad = item.get("cantidad")

        precio_unitario = buscar_precio(id_producto)
        if precio_unitario is None:
            return jsonify({"success": False, "message": f"No se encontró precio para el producto {id_producto}"})

        resultado_detalle = cargar_detalle_venta(id_venta, id_producto, cantidad, precio_unitario)
        if not resultado_detalle:
            return jsonify({"success": False, "message": f"Error al cargar detalle para el producto {id_producto}"})

    # 6. Descontar stock
    resultado_stock = descontar_stock_pedido(pedido)
    if not resultado_stock:
        return jsonify({"success": False, "message": "Venta cargada, pero no se pudo actualizar el stock"})

    # 7. Todo correcto
    return jsonify({"success": True, "message": "Venta cargada correctamente"})

############################### FUNCIÓN DE MENSAJES
def mensajes(resultado, mensaje_personalizado):
    """ MODULO DE MENSAJES GENERICO """
    if resultado == "Producto_No_Encontrado":
        flash("❌ Producto no encontrado. Verificá el código.", "error")
    elif resultado == "Stock_Insuficiente":
        flash("❌ Stock insuficiente para completar la venta.", "error")
    elif resultado == "ok":
        flash(mensaje_personalizado, "success")
    elif resultado == "Conexion_Error":
        flash("❌ Error de conexión con la base de datos.", "error")
    else:
        flash("❌ Ocurrió un error inesperado.", "error")
    