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
    
    validacion = verificar_datos(dni, nombre, fecha_nacimiento, puesto, estado, clave)
    
    if validacion != "ok":
        return validacion
    
    nombre = nombre.strip().title()
    
    conexion = get_connection()
    if conexion is None:
        return "Error_conexion" 

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
        return "ok"
    except Exception as e:
        print("Error al cargar usuario:", e)
        return 'Error_insertar'

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
    
    ############ Función de Verificar datos
def verificar_datos(dni, nombre, fecha_nacimiento, puesto, estado, clave):
    
    error = verificar_dni(dni)
    if error:
        return error
    
    if not nombre or len(nombre) < 3:
        return "Nombre_corto"
    
    error = verificar_nacimiento(fecha_nacimiento)
    if error:   
        return error
    
    if puesto not in ['cajero', 'vendedor', 'gerente', 'encargado_barra']:
        return "Puesto_invalido"
    
    if estado not in ['activo', 'inactivo', 'suspendido']:
        return "Estado_invalido"
    
    error = verificar_clave(clave)
    if error:
        return error    
    
    return "ok"

########### Funcion veridicar dni
def verificar_dni(dni):
    """ Verifica si el DNI es válido y único """
    if not dni or len(dni) < 7 or len(dni) > 8:
        return "DNI_invalido"
    
    usuario = obtener_un_usuario(dni)
    if usuario:
        return "DNI_existente"
    
    return False # DNI válido y único

########### Función verificar clave
def verificar_clave(clave):
    """ Verifica si la clave es válida """
    if not clave or len(clave) < 6:
        return "Clave_corta"
    
    if not any(char.isdigit() for char in clave):
        return "Clave_sin_numero"
    
    if not any(char.isupper() for char in clave):
        return "Clave_sin_mayuscula"
    
    if not any(char.islower() for char in clave):
        return "Clave_sin_minuscula"
    
    return None
    
############## Función OBTENER UN Usuario
def obtener_un_usuario(dni):
    """ Función para obtener un usuario por DNI """
    conexion = get_connection()
    if conexion is None:
        return None  # Devuelve None si falla la conexión

    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM public."usuarios" WHERE dni_usuario = %s', (dni,))
    usuario = cursor.fetchone()
    cursor.close()
    conexion.close()
    return usuario

############## Función VERIFICAR FECHA DE NACIMIENTO
def verificar_nacimiento(fecha_nacimiento):
    """ Verifica si la fecha de nacimiento es válida """
    if not fecha_nacimiento:
        return "Fecha_nacimiento_vacia"
    
    try:
        from datetime import datetime
        fecha = datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
        if fecha > datetime.now():
            return "Fecha_futura"
    except ValueError:
        return "Fecha_invalida"
    
    return None

########### Funcion para mensajes
def mensajes_usuario(codigo):
    """ Traduce los códigos de error a mensajes legibles """
    mensajes = {
        "DNI_invalido": "El DNI ingresado no es válido.",
        "DNI_existente": "Ya existe un usuario con ese DNI.",
        "Nombre_corto": "El nombre es demasiado corto.",
        "Fecha_nacimiento_vacia": "Debe ingresar la fecha de nacimiento.",
        "Fecha_invalida": "La fecha ingresada no es válida.",
        "Fecha_futura": "La fecha de nacimiento no puede ser en el futuro.",
        "Puesto_invalido": "Seleccione un puesto válido.",
        "Estado_invalido": "Seleccione un estado válido.",
        "Clave_corta": "La clave debe tener al menos 6 caracteres.",
        "Clave_sin_numero": "La clave debe contener al menos un número.",
        "Clave_sin_mayuscula": "La clave debe tener al menos una letra mayúscula.",
        "Clave_sin_minuscula": "La clave debe tener al menos una letra minúscula.",
        "Error_conexion": "Error de conexión con la base de datos.",
        "Error_insertar": "No se pudo insertar el usuario.",
        "ok": "Usuario cargado correctamente."
    }
    return mensajes.get(codigo, "Ocurrió un error desconocido.")