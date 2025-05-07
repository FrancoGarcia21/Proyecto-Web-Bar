from database.connection import get_connection

def obtener_productos():
    """ Función para obtener productos """
    conexion = get_connection()
    if conexion is None:
        return []  # Devuelve lista vacía si falla la conexión

    cursor = conexion.cursor()
    #cursor.execute("SELECT id_producto, nombre_producto, cantidad_stock, costo_unitario FROM 'Producto'")
    cursor.execute('SELECT * FROM public."Producto" ORDER BY id_producto ASC')
    productos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return productos
