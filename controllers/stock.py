from database.connection import get_connection

############## Función TODAS las Categorias
def obtener_categorias():
    """ Obtiene las categorias de la base """
    conexion = get_connection()
    if conexion is None:
        return "Conexion fallida"
    
    try:
        cursor = conexion.cursor()
        cursor.execute(""" 
                       SELECT * FROM public.categorias
                       """)
        categorias = cursor.fetchall()
        cursor.close()
        conexion.close()
        return categorias
    except Exception as e:
            print("Error al buscar productos:", e)
            return False


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

############## Función OBTENER productos segun UNA categoria
def obtener_productos_de_categoria(id_categoria):
    """ Función para obtener productos para una categoria """
    conexion = get_connection()
    if conexion is None:
        return []  # Devuelve lista vacía si falla la conexión

    try:
        cursor = conexion.cursor()
        cursor.execute(""" SELECT * FROM public."productos" WHERE id_categoria = %s """, (id_categoria,))
        productos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return productos
    except Exception as e:
            return False

############## Función CARGAR producto nuevo
def cargar_producto_nuevo(id_producto, nombre_producto, cantidad_stock, costo_unitario, limite_alarmante, id_categoria):
    """ Función para cargar productos nuevos """
    
    
    # Validaciones
    errores = validar_datos(id_producto, nombre_producto, cantidad_stock, costo_unitario, limite_alarmante)
    
    nombre_producto = nombre_producto.strip().title()  # Eliminar espacios al inicio y al final
    
    if errores is not None:
        return errores
    
    conexion = get_connection()
    if conexion is None:
        return "Conexion_Error"  
    
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO public."productos" (id_producto, nombre_producto, cantidad_stock, costo_unitario, limite_alarmante, id_categoria)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (id_producto, nombre_producto, cantidad_stock, costo_unitario, limite_alarmante, id_categoria))
        conexion.commit()
        cursor.close()
        conexion.close()
        return "ok"
    except Exception as e:
        print(f"Error al insertar producto: {e}")
        return 'error'
        
############## Función AGREGAR STOCK de un producto
def agregar_stock(id_producto, cantidad_stock):
    """ Función para agregar stock de un producto """

    # validar que cantidad stock no sea negativo
    if int(cantidad_stock) < 0:
        return "Cantidad_Negativa"

     # busco y sumo el producto nuevo
    un_producto = obtener_un_producto(id_producto)
    if not un_producto:
        return "Producto_No_Encontrado"
        
    cantidad_stock = int(cantidad_stock) + int(un_producto[3]) # el 3 es porque es la 3er columna de la tabla

    return modificar_stock(id_producto, cantidad_stock)

############### Función que MODIFICA el stock de un producto (conexion a base de datos)
def modificar_stock(id_producto, cantidad_stock):
    """ Funcion que llama a la base y carga el dato nuevo del stock """
    conexion = get_connection()
    if conexion is None:
        return "Conexion_Error"
    
    try:
        
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE public.productos
            SET cantidad_stock = %s
            WHERE id_producto = %s
        """, (cantidad_stock ,id_producto))
        conexion.commit()
        cursor.close()
        conexion.close()
        return "ok"
    except Exception as e:
        return "error"

############## Función MODIFICAR ESTADO de un producto
def modificar_estado(id_producto, estado):
    """ Función para modificar el estado en la base """
    conexion = get_connection()
    
    if conexion is None:
        return "conexion_error"
    
    try:
        # busco y sumo el producto nuevo
        un_producto = obtener_un_producto(id_producto)
        if not un_producto:
            return "Producto_No_Encontrado"
        
        cursor = conexion.cursor()
        cursor.execute(
            """ UPDATE public."productos" 
                SET estado = %s
                WHERE id_producto = %s
            """, (estado, id_producto)
        )
        conexion.commit()
        cursor.close()
        conexion.close()
        return "ok"
    except Exception as e:
        return "error"

############## Función para VERIFICAR el stock de un producto
def verificar_stock(pedido):
    """ Función que verifica si un producto tiene stock antes de hacer la venta """
    conexion = get_connection()
    if conexion is None:
        return "conexion_error"

    errores = []

    for item in pedido:
        id_producto = str(item.get('id'))
        cantidad_vendida = item.get('cantidad')

        # Obtengo el producto
        un_producto = obtener_un_producto(id_producto)
        if not un_producto:
            return {"estado": False, "error": "Producto No Encontrado con id: " + str(id_producto)}

        cantidad_stock = un_producto[3] # la 3er columna es cantidad_stock
        if cantidad_stock < cantidad_vendida:
            errores.append(f"Stock insuficiente para el producto: {un_producto[2]}. Stock actual: {cantidad_stock}, cantidad vendida: {cantidad_vendida}")
            
    if errores:
        # Si hay errores, los concateno en un string
        error_mensaje = " | ".join(errores)
        return {"estado": False, "error": error_mensaje}
        
    return {"estado": True, "error": "Stock suficiente"}


################ Función para CALCULAR el valor total de un pedido
def calcular_valor_total(pedido):
    """ Función que calcula el valor total de un pedido """
    valor_total = 0
    for item in pedido:
        id_producto = str(item.get('id'))
        cantidad_vendida = item.get('cantidad')

        # Obtengo el producto
        un_producto = obtener_un_producto(id_producto)
        if not un_producto:
            continue  # Si no se encuentra el producto, lo ignoro

        costo_unitario = un_producto[4]  # la 4ta columna es costo_unitario
        valor_total += costo_unitario * cantidad_vendida
        
    return valor_total
    
################ Función para DESCONTAR el stock
def descontar_stock(producto):
    """ Función que descuenta una cierta cantidad al stock """

    id_producto = str(producto.get('id'))
    cantidad_vendida = producto.get('cantidad')
    
    producto_en_base = obtener_un_producto(id_producto)
    
    cantidad_final = int(producto_en_base[3]) - int(cantidad_vendida)  # la 3er columna es cantidad_stock
    
    return modificar_stock(id_producto, cantidad_final)
    
   

############### Función descontar stock de un peiddo
def descontar_stock_pedido(pedido):
    """ Funcion que descuenta el stock de todos los productos de un pedido """
    for item in pedido:
        resultado = descontar_stock(item)
        if resultado != "ok":
            return False
    return True

############### Funcion para buscar el precio de un producto
def buscar_precio(id_producto):
    """ Función que busca el precio de un producto """
    un_producto = obtener_un_producto(str(id_producto))
    if not un_producto:
        return None  # Si no se encuentra el producto, retorno None

    return un_producto[4]  # la 4ta columna es costo_unitario

################ Función para validar los datos 
def validar_datos(id_producto, nombre_producto, cantidad_stock, costo_unitario, limite_alarmante):
    """ Función para validar los datos de un producto """
    
    error = validar_id_producto(id_producto)
    if error is not None:
        return error
    
    error = validar_nombre_producto(nombre_producto)
    if error is not None:
        return error
    
    for campo in [cantidad_stock, costo_unitario, limite_alarmante]:
        error = validar_numero_positivo(campo)
        if error:
            return error
    
    # Si todas las validaciones pasan, retorno 
    return error
    
############## VALIDACIONES DE DATOS SEPARADOS 

############# Validar ID  
def validar_id_producto(id_producto):
    """ Valida si el id existe, si no existe retorne None """
  
    if obtener_un_producto(str(id_producto)) is not None:
        return ["Producto_Existente"]
    return None
    
############# Validar Nombre
def validar_nombre_producto(nombre_producto):
    """ Valida si el nombre ya existe en la base """
    
    nombre =  f'%{nombre_producto}%'
    
    conexion = get_connection()
    if conexion is None:
        return "Conexion_Error"
    
    try:
        cursor = conexion.cursor()
        cursor.execute(""" 
                       SELECT EXISTS (SELECT 1 FROM public."productos" WHERE nombre_producto ILIKE  %s )
                       """, (nombre,))
        existe = cursor.fetchone()[0] # porque aca devuelve un boleana como [true, ] por el select Exist
        cursor.close()
        conexion.close()
        
        if existe:
            return ["Nombre_Producto_Existente"]
        return None
    except Exception as e:
            print("Error al validar nombre de producto:", e)
            return False
        
############# Validar Cantidad
def validar_numero_positivo(cantidad):
    """ Valido que la cantidad sea positiva """
    
    try:
        if int(cantidad) < 0:
            return ["Cantidad_Negativa"]
        return None
    except (ValueError, TypeError):
        return ["Cantidad_Invalida"]

