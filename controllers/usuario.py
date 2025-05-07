from database.connection import get_connection

def obtener_usuarios():
    """ Función para obtener usuarios """
    conexion = get_connection()
    if conexion is None:
        return []  # Devuelve lista vacía si falla la conexión

    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM public."Usuario"')
    usuarios = cursor.fetchall()
    cursor.close()
    conexion.close()
    return usuarios