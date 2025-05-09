from database.connection import get_connection

############## Función OBTENER UN producto
def obtener_un_producto(id_producto):
    """ Función para obtener un solo producto """
    conexion = get_connection()
    if conexion is None:
        return []  # Devuelve lista vacía si falla la conexión

    try:
        cursor = conexion.cursor()
        cursor.execute(""" 
                       SELECT * FROM public."productos" WHERE id_producto = %s
                       """, (id_producto,))
        producto = cursor.fetchone()
        cursor.close()
        conexion.close()
        return producto
    except Exception as e:
            print("Error al buscar productos:", e)
            return False

############## Función OBTENER productos
def obtener_productos():
    """ Función para obtener productos """
    conexion = get_connection()
    if conexion is None:
        return []  # Devuelve lista vacía si falla la conexión

    try:
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM public."productos" ORDER BY id_producto ASC')
        productos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return productos
    except Exception as e:
            print("Error al buscar productos:", e)
            return False

############## Función CARGAR producto nuevo
def cargar_producto_nuevo(id_producto, nombre_producto, cantidad_stock, costo_unitario, limite_alarmante, id_categoria):
    """ Función para cargar productos nuevos """
    conexion = get_connection()
    if conexion is None:
        return []  
    
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO public."productos" (id_producto, nombre_producto, cantidad_stock, costo_unitario, limite_alarmante, id_categoria)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (id_producto, nombre_producto, cantidad_stock, costo_unitario, limite_alarmante, id_categoria))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception as e:
            print("########## ERROR AL CARGAR EL PRODUCTO al cargar producto: ###############3", e)
            return False
        
############## Función MODIFICAR STOCK de un producto
def modificar_stock(id_producto, cantidad_stock):
    """ Función para modificar stock de un producto """
    conexion = get_connection()
    if conexion is None:
        return []
    
    try:
        # busco y sumo el producto nuevo
        un_producto = obtener_un_producto(id_producto)
        if not un_producto:
            print("Producto no encontrado")
            return False
        
        cantidad_stock = int(cantidad_stock) + int(un_producto[3]) # el 3 es porque es la 3er columna de la tabla

        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE public.productos
            SET cantidad_stock = %s
            WHERE id_producto = %s
        """, (cantidad_stock ,id_producto))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception as e:
        print("############# ERROR AL MODIFICAR EL STOCK: ", e)
        return False