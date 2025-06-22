from flask import Blueprint, render_template, request
from utils.decoradores import login_required, role_required
import psycopg2
import os

informe_bp = Blueprint('informe', __name__)

# Función para conectar a la base de datos usando variables del entorno
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

# Vista principal del informe (sin mostrar sección)
@informe_bp.route('/informe')
@login_required
@role_required('administrador')
def informe():
    return render_template('informe.html', tipo=None)

# Vista con tabla de ventas paginada
@informe_bp.route('/informe/ventas')
@login_required
@role_required('administrador')
def informe_ventas():
    page = int(request.args.get('page', 1))         # Página actual desde query string (por defecto 1)
    per_page = 15                                   # Cantidad de registros por página
    offset = (page - 1) * per_page                  # OFFSET para la query

    conn = get_db_connection()
    cur = conn.cursor()

    # Consulta paginada
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

    # Contar total de registros para calcular la cantidad de páginas
    cur.execute("SELECT COUNT(*) FROM detalle_venta;")
    total_registros = cur.fetchone()[0]

    cur.close()
    conn.close()

    total_paginas = (total_registros + per_page - 1) // per_page

    return render_template(
        'informe.html',
        tipo='ventas',
        ventas=ventas,
        page=page,
        total_paginas=total_paginas
    )

# Vista con texto plano (placeholder para informe por usuario)
@informe_bp.route('/informe/usuario')
@login_required
@role_required('administrador')
def informe_usuario():
    return render_template('informe.html', tipo='usuario')
