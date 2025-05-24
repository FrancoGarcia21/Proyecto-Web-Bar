from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.stock import obtener_productos, cargar_producto_nuevo,modificar_stock, modificar_estado, obtener_categorias
from utils.decoradores import login_required, role_required
import logging

logging.basicConfig(level=logging.DEBUG)

stock_bp = Blueprint('stock', __name__)

############################### Ruta  de MOSTRAR lista de productos
@stock_bp.route('/stock')
@login_required
@role_required('administrador')
def stock():
    """ Muestra el stock """
    productos = obtener_productos()
    categorias = obtener_categorias()
    return render_template('stock.html', productos=productos, categorias=categorias, mostrar='lista')


############################### Ruta de CARGAR producto
@stock_bp.route('/stock/cargar', methods=['POST'])
@login_required
@role_required('administrador')
def cargar_producto_nuevo_route():
    """ Ruta para cargar un producto nuevo """
    id_producto = request.form.get('producto')
    nombre_producto = request.form.get('nombreProducto')
    cantidad_stock = int(request.form.get('cantidad'))
    costo_unitario = request.form.get('costo')
    limite_alarmante = int(request.form.get('limite'))
    id_categoria = request.form.get('categoria')
    
    resultado = cargar_producto_nuevo(id_producto, nombre_producto, cantidad_stock, costo_unitario, limite_alarmante, id_categoria)

    mensajes(resultado, "✅ PRODUCTO AGREGADO CORRECTAMENTE.")

    return redirect(url_for('stock.stock'))

############################### Ruta AGREGAR STOCK
@stock_bp.route('/stock/modificarStock', methods=['POST'])
@login_required
@role_required('administrador')
def modificar_stock_route():
    """ Ruta para modificar el stock"""
    id_producto = request.form.get('producto')
    cantidad_stock = request.form.get('cantidad')
    
    resultado = modificar_stock(id_producto, cantidad_stock)
    
    mensajes(resultado, "✅ STOCK MODIFICADO CORRECTAMENTE.")
    
    return redirect(url_for('stock.stock'))

############################### FUNCIÓN DE MENSAJES
@stock_bp.route('/stock/modificar_estado', methods=['POST'])
@login_required
@role_required('administrador')
def modificar_estado_route():
    """ Ruta para modificar estado """
    id_producto = request.form.get('producto')
    estado = request.form.get('estado')
    
    resultado = modificar_estado(id_producto, estado)
    
    mensajes(resultado, "✅ ESTADO MODIFICADO CORRECTAMENTE.")

    return redirect(url_for('stock.stock'))


############################### FUNCIÓN DE MENSAJES
def mensajes(resultado, mensaje_personalizado):
    """ MODULO DE MENSAJES GENERICO """
    if resultado == "Producto_No_Encontrado":
        flash("❌ Producto no encontrado. Verificá el código.", "error")
    elif resultado == "ok":
        flash(mensaje_personalizado, "success")
    elif resultado == "Conexion_Error":
        flash("❌ Error de conexión con la base de datos.", "error")
    else:
        flash("❌ Ocurrió un error inesperado.", "error")
    