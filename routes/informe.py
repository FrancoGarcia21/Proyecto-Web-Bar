from flask import Blueprint, render_template, request
from utils.decoradores import login_required, role_required
import psycopg2
import os

# Crear Blueprint
informe_bp = Blueprint('informe', __name__)

# Función de conexión a la base de datos
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

# Página inicial de informes (sin contenido aún)
@informe_bp.route('/informe')
@login_required
@role_required('administrador')
def informe():
    return render_template('informe.html', tipo=None)

# Informe de ventas paginado
@informe_bp.route('/informe/ventas')
@login_required
@role_required('administrador')
def informe_ventas():
    # Obtener número de página desde la query (?page=)
    page = int(request.args.get('page', 1))
    per_page = 10  # Cantidad de resultados por página
    offset = (page - 1) * per_page

    # Conectar a la base de datos
    conn = get_db_connection()
    cur = conn.cursor()

    # Consulta principal paginada
    cur.execute("""
        SELECT 
            v.fecha_venta,
            u.nombre AS nombre_usuario,
            p.nombre_producto,
            dv.cantidad,
            dv.precio_unitario,
            (dv.cantidad * dv.precio_unitario) AS subtotal
        FROM ventas v
        JOIN detalle_venta dv ON v.id_venta = dv.id_venta
        JOIN productos p ON dv.id_producto::TEXT = p.id_producto
        JOIN usuarios u ON v.dni_usuario = u.dni_usuario
        ORDER BY v.fecha_venta DESC
        LIMIT %s OFFSET %s;
    """, (per_page, offset))
    
    ventas = cur.fetchall()

    # Calcular total de registros para la paginación
    cur.execute("SELECT COUNT(*) FROM detalle_venta;")
    total_registros = cur.fetchone()[0]
    total_paginas = (total_registros + per_page - 1) // per_page  # Redondeo hacia arriba

    # Cerrar conexión
    cur.close()
    conn.close()

    return render_template(
        'informe.html',
        tipo='ventas',
        ventas=ventas,
        page=page,
        total_paginas=total_paginas
    )

# Informe de usuarios (placeholder)
@informe_bp.route('/informe/usuario')
@login_required
@role_required('administrador')
def informe_usuario():
    return render_template('informe.html', tipo='usuario')
