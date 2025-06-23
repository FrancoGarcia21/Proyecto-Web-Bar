from flask import Blueprint, render_template, request, jsonify
from utils.decoradores import login_required, role_required
import psycopg2
import os
from datetime import date
from psycopg2.extras import RealDictCursor

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

# Página inicial de informes → muestra solo el gráfico del día
from datetime import timedelta, datetime

@informe_bp.route('/informe')
@login_required
@role_required('administrador')
def informe():
    return render_template('informe.html', tipo='ventas_ultimos_7')

# Informe de ventas paginado (tabla completa)
@informe_bp.route('/informe/ventas')
@login_required
@role_required('administrador')
def informe_ventas():
    page = int(request.args.get('page', 1))
    per_page = 10
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cur = conn.cursor()

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

    cur.execute("SELECT COUNT(*) FROM detalle_venta;")
    total_registros = cur.fetchone()[0]
    total_paginas = (total_registros + per_page - 1) // per_page

    cur.close()
    conn.close()

    return render_template(
        'informe.html',
        tipo='ventas',
        ventas=ventas,
        page=page,
        total_paginas=total_paginas
    )

# API: Ventas del día agrupadas por hora
@informe_bp.route('/api/ventas/hoy')
@login_required
@role_required('administrador')
def api_ventas_hoy():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    hoy = date.today()
    desde = datetime.combine(hoy, datetime.min.time()) - timedelta(hours=6)  # Ayer a las 18:00
    hasta = datetime.combine(hoy, datetime.min.time()) + timedelta(hours=4)  # Hoy a las 04:00

    cur.execute("""
        SELECT 
            TO_CHAR(DATE_TRUNC('hour', v.fecha_venta), 'HH24:00') AS hora,
            SUM(dv.cantidad * dv.precio_unitario) AS total
        FROM ventas v
        JOIN detalle_venta dv ON v.id_venta = dv.id_venta
        WHERE v.fecha_venta BETWEEN %s AND %s
        GROUP BY hora
        ORDER BY hora;
    """, (desde, hasta))

    resultados = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(resultados)


@informe_bp.route('/api/ventas/rango')
@login_required
@role_required('administrador')
def api_ventas_rango():
    inicio = request.args.get('inicio')
    fin = request.args.get('fin')
    if not inicio or not fin:
        return jsonify([])

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("""
        SELECT 
            fecha_venta::TEXT AS dia,
            SUM(valor_total) AS total
        FROM ventas
        WHERE fecha_venta BETWEEN %s AND %s
        GROUP BY fecha_venta
        ORDER BY fecha_venta;
    """, (inicio, fin))

    resultados = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(resultados)

@informe_bp.route('/api/ventas/ultimos7')
@login_required
@role_required('administrador')
def api_ventas_ultimos7():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    hoy = date.today()
    hace_7 = hoy - timedelta(days=6)  # incluye hoy
    cur.execute("""
        SELECT 
            TO_CHAR(fecha_venta, 'YYYY-MM-DD') AS dia,
            SUM(valor_total) AS total
        FROM ventas
        WHERE fecha_venta BETWEEN %s AND %s
        GROUP BY dia
        ORDER BY dia;
    """, (hace_7, hoy))

    resultados = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(resultados)


# Informe de usuarios (placeholder)
@informe_bp.route('/informe/usuario')
@login_required
@role_required('administrador')
def informe_usuario():
    return render_template('informe.html', tipo='usuario')
