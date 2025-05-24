import bcrypt

from database.connection import get_connection


############## Función OBTENER Usuarios
def obtener_usuarios():
    """ Función para obtener usuarios """
    conexion = get_connection()
    if conexion is None:
        return []  # Devuelve lista vacía si falla la conexión

    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM public."usuarios"')
    usuarios = cursor.fetchall()
    cursor.close()
    conexion.close()
    return usuarios

############## Función CARGAR usuario
def cargar_usuario(dni, nombre, fecha_nacimiento, puesto, estado, clave):
    """ Función para gargar un usuario en la base """
    conexion = get_connection()
    if conexion is None:
        return False

    try:
        # Encripto la clave
        hashed_password = bcrypt.hashpw(clave.encode('utf-8'), bcrypt.gensalt())
        
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO public."usuarios" (dni_usuario, nombre, fecha_nacimiento, tipo_usuario, estado, clave)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (dni, nombre, fecha_nacimiento, puesto, estado, hashed_password.decode('utf-8')))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception as e:
        print("Error al cargar usuario:", e)
        return False

############## Función MODIFICAR ESTADO usuarios
def modificar_estado_usuario(dni, estado):
    """ Función que modifica el estado en la base """
    conexion = get_connection()
    
    if conexion is None:
        return False
    
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE public.usuarios
            SET estado = %s
            WHERE dni_usuario = %s
        """, (estado, dni))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception as e:
        print( "Error al modificar Usuario: ", e)
        return False
    
    