""" importaciones """

import bcrypt

from database.connection import get_connection


############## Función validar un usuario
def verificacion_usuario(id_usuario, password):
    """ Función para validar un producto"""
    conexion = get_connection()
    if conexion is None:
        return 'Conexion_Error'

    try:
        cursor = conexion.cursor()
        cursor.execute("""
                       SELECT clave FROM public.usuarios WHERE dni_usuario = %s
                       """, (id_usuario,))
        clave = cursor.fetchone()
        cursor.close()
        conexion.close()
        
        if clave is None:
          return "false"
        
        clave_hasheada = clave[0].encode('utf-8')
        print(clave, clave_hasheada)
        
        if bcrypt.checkpw(password.encode('utf-8'), clave_hasheada):
            return "ok"
        else:
            return "false"
        
    except Exception as e:
            print("Error al buscar productos:", e)
            return "ERROR"